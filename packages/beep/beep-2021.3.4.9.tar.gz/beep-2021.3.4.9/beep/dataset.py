# Copyright [2020] [Toyota Research Institute]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module and scripts for assembling a ML model training dataset using BeepFeatures objects

Options:
    -h --help        Show this screen
    --fit            <true_or_false>  [default: False] Fit model
    --version        Show version


The `dataset` script will assemble a BeepDataset object for ML model training
It stores its outputs in `/data-share/datasets/`


"""
from __future__ import division
import os
import pandas as pd
import numpy as np
from monty.json import MSONable
from monty.serialization import loadfn, dumpfn
from functools import reduce
from beep import MODULE_DIR
from beep.utils import parameters_lookup
from beep.featurize import (
    RPTdQdVFeatures, HPPCResistanceVoltageFeatures,
    HPPCRelaxationFeatures, DiagnosticProperties,
    DiagnosticSummaryStats
)
from sklearn.model_selection import train_test_split
from scipy import interpolate

FEATURE_HYPERPARAMS = loadfn(
    os.path.join(MODULE_DIR, "features/feature_hyperparameters.yaml")
)

FEATURIZER_CLASSES = [RPTdQdVFeatures, HPPCResistanceVoltageFeatures,
                      HPPCRelaxationFeatures, DiagnosticSummaryStats,
                      DiagnosticProperties]


class BeepDataset(MSONable):
    """
    Class corresponding to a training dataset assembled from BeepFeatures objects

    Attributes:
            name (str): name of the dataset
            data (pd.DataFrame): dataframe composed of different features concatenated column-wise and
            different runs concatenated row-wise
            metadata (list): list of metadata dicts for the different feature objects
            filenames (list): list of filenames that have atleast one of the feature objects
            feature_sets (dict): dictionary with feature class names as keys, and feature labels as values
            dataset_dir (str): path to store serialized dataset
            train_cells_parameter_dict (dict): Dictionary with keys corresponding to unique identifiers for runs that
                are part of the training dataset, and values being a dictionary of project parameters for the run
            test_cells_parameter_dict (dict): Dictionary with keys corresponding to unique identifiers for runs that
                are part of the test dataset, and values being a dictionary of project parameters for the run
            X_train (pd.DataFrame): Training dataset predictors
            X_test (pd.DataFrame): Test dataset predictors
            y_train (pd.DataFrame): Training dataset outcomes
            y_test (pd.DataFrame): Test dataset outcomes
            missing (pd.DataFrame): Feature sets that could not be found, or not be initialized because
             the ProcessedCyclerRun object did not meet the necessary validation criteria.

    """

    def __init__(self, name, data, metadata, filenames, feature_sets, dataset_dir='data-share/datasets', missing=None):

        """
        Invokes BeepDataset object

        Args:
            name (str): name of the dataset
            data (pd.DataFrame): dataframe composed of different features concatenated column-wise and
            different runs concatenated row-wise
            metadata (list): list of metadata dicts for the different feature objects
            filenames (list): list of filenames that have atleast one of the feature objects
            feature_sets (dict): dictionary with feature class names as keys, and feature labels as values
            dataset_dir (str): path to store serialized dataset
            missing (pd.DataFrame): Feature sets that could not be found, or not be initialized because
             the ProcessedCyclerRun object did not meet the necessary validation criteria.
        """
        self.name = name
        self.data = data
        self.metadata = metadata
        self.filenames = filenames
        self.feature_sets = feature_sets
        self.dataset_dir = dataset_dir
        self.train_cells_parameter_dict = {}
        self.test_cells_parameter_dict = {}
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.missing = missing

    def as_dict(self):
        """
        Method for dictionary serialization
        Returns:
            dict: corresponding to dictionary for serialization
        """
        obj = {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
            "name": self.name,
            "data": self.data.to_dict("list"),
            "metadata": self.metadata,
            "filenames": self.filenames,
            "dataset_dir": self.dataset_dir,
            "feature_sets": self.feature_sets,
            "missing": self.missing.to_dict("list")
        }
        return obj

    @classmethod
    def from_dict(cls, d):
        """MSONable deserialization method"""
        d["data"] = pd.DataFrame(d["data"])
        d["missing"] = pd.DataFrame(d["missing"])
        d["filenames"] = list(d["filenames"])
        return cls(**d)

    @classmethod
    def from_features(cls, name, project_list=['PreDiag'], feature_class_list=FEATURIZER_CLASSES,
                      feature_dir="data-share/features/", dataset_dir="data-share/datasets"):
        """
        Method to assemble a dataset from a list of BeepFeatures objects generated for one or more projects. 

        project_list (list): list of projects from which training data will be assembled
        feature_class_list (list): list of BeepFeatures classes
        feature_dir (str): Root directory for features. Assumes that all objects belonging to a feature class
            are stored in a folder <feature_dir>/<MyFeatureSet.class_feature_name>
        dataset_dir (str): path to store serialized dataset

        Returns:
            beep.BeepDataset object
        """
        feature_df_list = []
        metadata = []
        feature_sets = {}
        missing = pd.DataFrame(columns=['filename', 'feature_class'])

        for feature_class in feature_class_list:
            feature_path = os.path.join(feature_dir, feature_class.class_feature_name)
            if os.path.isdir(feature_path):
                feature_df = pd.DataFrame()
                for project in project_list:
                    feature_jsons = [os.path.join(feature_path, f) for f in os.listdir(feature_path) if
                                     (os.path.isfile(os.path.join(feature_path, f)) and
                                      f.startswith(project))]
                    feature_jsons.sort()
                    for feature_json in feature_jsons:
                        obj = loadfn(feature_json)
                        df = obj.X
                        df['file'] = obj.metadata['protocol'].split('.')[0]
                        # seq_num computation assumes file naming follows the convention:
                        # ProjectName_SeqNum_Channel_ObjectName.json
                        df['seq_num'] = int(os.path.basename(feature_json).split('_')[1])
                        feature_df = pd.concat([feature_df, df]).reset_index(drop=True)
                        # TODO: Need some logic for ensuring that features of a given class being concatenated
                        # row-wise have the same metadata dict

                feature_df_list.append(feature_df)
                feature_sets[feature_class.class_feature_name] = list(feature_df.columns)

            else:
                missing.loc[len(missing)] = \
                    ['', feature_class.class_feature_name]

        df = reduce(lambda x, y: pd.merge(x, y, on=['file', 'seq_num'], how='outer'), feature_df_list)
        # Outer-join used so that even partially featurized cells can be loaded into dataset
        # NaNs imputation to be done downstream by the user

        return cls(name, df, metadata, df.file.unique(), feature_sets, dataset_dir, missing)

    @classmethod
    def from_processed_cycler_runs(cls, name, project_list, processed_run_list=None,
                                   feature_class_list=FEATURIZER_CLASSES,
                                   hyperparameter_dict=None, processed_dir="data-share/structure/",
                                   feature_dir="data-share/features/",
                                   dataset_dir="data-share/datasets",
                                   parameters_path="data-share/raw/parameters"):
        """
        Method to assemble a dataset directly from a list of ProcessedCyclerRun objects

        Arguments:
            project_list (list): list of projects to featurize and combine as a training dataset
            processed_run_list: (list) list of paths to specific ProcessedCyclerRun objects to be featurized.
                If provided, this will over-ride project based looping.
            feature_class_list: list of BeepFeatures objects to invoke on the structured cycler files.
            hyperparameter_dict (dict): dictionary with keys belonging to feature_class_list, and values being
                a list of hyperparam dictionaries for that feature_class. List allows multiple instances of the
                same BeepFeatures class to be created and assembled into the training dataset
            processed_dir (str): root directory storing structure jsons (ProcessedCyclerRun objects)
            feature_dir (str): root directory for features (BeepFeatures objects)
            dataset_dir (str): location to store dataset

        Returns:
            beep.BeepDataset object
        """
        feature_sets = {}
        failed_featurizations = pd.DataFrame(columns=['filename', 'feature_class'])

        # If no metadata is provided, assume defaults
        if hyperparameter_dict is None:
            hyperparameter_dict = {}
            print('No hyperparameters specified for feature generation. Assuming defaults and proceeding.')
            for feature_class in feature_class_list:
                if feature_class.class_feature_name in FEATURE_HYPERPARAMS.keys():
                    hyperparameter_dict[feature_class.class_feature_name] = \
                        [FEATURE_HYPERPARAMS[feature_class.class_feature_name]]
                else:
                    hyperparameter_dict[feature_class.class_feature_name] = None
        else:
            for feature_class in feature_class_list:
                # if a specific feature class has a missing hyperparameter dict, initialize with defaults
                if hyperparameter_dict[feature_class.class_feature_name] is None:
                    print('Assuming default hyperparameter dictionary for',
                          feature_class.class_feature_name)
                    if feature_class.class_feature_name in FEATURE_HYPERPARAMS.keys():
                        hyperparameter_dict[feature_class.class_feature_name] = \
                            [FEATURE_HYPERPARAMS[feature_class.class_feature_name]]
                    else:
                        hyperparameter_dict[feature_class.class_feature_name] = None
                # if the provided hyperparameter dictionary has the wrong keys, raise error
                elif set(FEATURE_HYPERPARAMS[feature_class.class_feature_name].keys()) != \
                        set(hyperparameter_dict[feature_class.class_feature_name][0].keys()):
                    raise ValueError('Invalid hyperparameter dictionary for' +
                                     feature_class.class_feature_name)

        # If a list of paths to ProcessedCyclerRun objects is not provided, then use all
        # files belonging to a project in <processed_dir>.
        if processed_run_list is None:
            processed_run_list = [os.path.join(processed_dir, f)
                                  for f in os.listdir(processed_dir)
                                  for project in project_list
                                  if (os.path.isfile(os.path.join(processed_dir, f)) and
                                      f.startswith(project) and
                                      f.endswith('structure.json'))]
        # feature_df_list is a list of dataframes. Each dataframe in it
        feature_df_list = [pd.DataFrame()]*sum([len(x) for x in hyperparameter_dict.values()])

        for processed_json in processed_run_list:
            processed_cycler_run = loadfn(processed_json)
            idx = 0
            for feature_class in feature_class_list:
                # For a given feature_class, loop through multiple hyperparameter combinations, if provided.
                for d in hyperparameter_dict[feature_class.class_feature_name]:
                    obj = feature_class.from_run(processed_json, feature_dir, processed_cycler_run,
                                                 d, parameters_path=parameters_path)
                    if obj:
                        df = obj.X
                        df['file'] = obj.metadata['protocol'].split('.')[0]
                        df['seq_num'] = int(os.path.basename(processed_json).split('_')[1])
                        feature_df_list[idx] = pd.concat([feature_df_list[idx], df]).reset_index(drop=True)
                    else:
                        failed_featurizations.loc[len(failed_featurizations)] = \
                            [os.path.split(processed_json)[1], feature_class.class_feature_name]
                    idx += 1

        for idx, feature_class in enumerate(feature_class_list):
            feature_sets[feature_class.class_feature_name] = list(feature_df_list[idx].columns)

        df = reduce(lambda x, y: pd.merge(x, y, on=['file', 'seq_num'], how='outer'), feature_df_list)
        return cls(name, df, hyperparameter_dict, df.file.unique(), feature_sets, dataset_dir, failed_featurizations)

    def generate_train_test_split(self, predictors=None, outcomes=None,
                                  split_by_cell=True, test_size=0.4, seed=123,
                                  parameters_path="data-share/raw/parameters"):
        """
        Method that subsets self.data into training and test datasets. Requires specification of columns to use as
        predictors and outcomes.

        Args:
            predictors (list): list of columns to use as predictors
            outcomes (list): list of columns to use as outcomes
            split_by_cell (bool): If True, train-test split on a per-run basis (self.filenames). Useful when
                there are multiple data-points per cell to avoid data-leaks between train and test data.
            seed (int): seed to ensure reproducible 'randomization'
            parameters_path (str): Root directory storing project parameter files. Assumes that parameter files
                begin with project name

        Returns:
            pd.DataFrame: X_train, X_test, y_train, y_test
        """

        if predictors is None:
            raise ValueError('Specify one or more predictor columns')

        if outcomes is None:
            raise ValueError('Specify one or more outcomes')

        np.random.seed(seed)
        if split_by_cell:
            test_cells = np.random.choice(self.filenames, int(len(self.filenames) * test_size))
            train_cells = [x for x in self.filenames if x not in test_cells]

            self.X_train = self.data.loc[self.data.file.isin(train_cells), predictors]
            self.X_test = self.data.loc[self.data.file.isin(test_cells), predictors]

            self.y_train = self.data.loc[self.data.file.isin(train_cells), outcomes]
            self.y_test = self.data.loc[self.data.file.isin(test_cells), outcomes]
        else:
            self.X_train, self.X_test, self.y_train, self.y_test = \
                train_test_split(self.data[predictors], self.data[outcomes], test_size, random_state=seed)

        if parameters_path is not None:
            self.train_cells_parameter_dict = get_parameter_dict(train_cells, parameters_path)
            self.test_cells_parameter_dict = get_parameter_dict(test_cells, parameters_path)

        return self.X_train, self.X_test, self.y_train, self.y_test

    def serialize(self):
        """
        Method to serialize dataset

        Args:
            processed_dir (dict): target directory.

        Returns:
             Path to serialized dataset

        """
        if not os.path.exists(self.dataset_dir):
            os.makedirs(self.dataset_dir)
        dumpfn(self, os.path.join(self.dataset_dir, self.name))
        return self.dataset_dir


def get_threshold_targets(dataset_diagnostic_properties,
                          cycle_type="rpt_1C",
                          metric="discharge_energy",
                          threshold=0.80,
                          filter_kinks=None,
                          extrapolate_threshold=True):
    """
    Method to generate a data frame with cycle number and throughputs at which the cell drops below a fractional metric.
    The metric being used is set by the basis variable and the value of the threshold can be varied. The cycle being
    used to evaluate the factional metric can be set be cycle_type_target. The point at which the cell crosses the
    threshold is determined with a linear interpolation between diagnostic cycles. In the event that the cell has not
    yet reached the threshold, the point at which it is expected to reach the threshold can be calculated by linear
    extrapolation from the last two diagnostic cycles. The filter kinks option allows for removal of cells with an
    abrupt change in degradation rate, possibly indicating some error or problem with the experiment.

    Args:
        dataset_diagnostic_properties (BeepDataset.data): Data attribute of dataset object created from the
            DiagnosticProperties feature
        cycle_type (str): Type of diagnostic cycle being used to measure the fractional metric
        metric (str): The metric being used for fractional capacity
        threshold (float): Value for the fractional metric to be considered above or below threshold
        filter_kinks (float): If set, cutoff value for the second derivative of the fractional metric (cells with an
            abrupt change in degradation rate might have something else going on). Typical value might be 0.04
        extrapolate_threshold (bool): Should threshold crossing point be extrapolated for cells that have not yet
            reached the threshold (warning: this uses a linear extrapolation from the last two diagnostic cycles)

    Returns:
         pd.DataFrame: Each row is a seq_num and contains the interpolated throughput and cycle number at which
            that particular run crossed the threshold.

    """
    threshold_values_df_list = []
    # Only use the target cycle type and basis for calculation
    cycle_type_target_df = dataset_diagnostic_properties[dataset_diagnostic_properties.cycle_type == cycle_type]
    cycle_type_target_df = cycle_type_target_df[cycle_type_target_df['metric'] == metric]

    for indx, run in enumerate(dataset_diagnostic_properties['file'].unique()):
        # Look at one run at a time
        run_target_df = cycle_type_target_df[cycle_type_target_df['file'] == run]

        # Filter to truncate data from cells that have a sudden drop in the fractional metric
        # (something wrong with the test)
        if filter_kinks and np.any(run_target_df['fractional_metric'].diff().diff() < filter_kinks):
            last_good_cycle = run_target_df[run_target_df['fractional_metric'].diff().diff() < filter_kinks][
                'cycle_index'].min()
            #         print(last_good_cycle)
            run_target_df = run_target_df[run_target_df['cycle_index'] < last_good_cycle]

        x_throughput_axis = run_target_df['normalized_regular_throughput']
        x_cycle_axis = run_target_df['cycle_index']
        y_interpolation_axis = run_target_df['fractional_metric']

        # Logic around how to deal with cells that have not crossed the threshold
        if run_target_df['fractional_metric'].min() > threshold and not extrapolate_threshold:
            print(run, " has not crossed threshold and extrapolation is off")
            continue
        elif run_target_df['fractional_metric'].min() > threshold and extrapolate_threshold:
            fill_value = "extrapolate"
            bounds_error = False
            x_throughput_linspace = np.linspace(x_throughput_axis.min(), 2 * x_throughput_axis.max(), num=1000)
            x_cycle_linspace = np.linspace(x_cycle_axis.min(), 2 * x_cycle_axis.max(), num=1000)
        else:
            fill_value = np.nan
            bounds_error = True
            x_throughput_linspace = np.linspace(x_throughput_axis.min(), x_throughput_axis.max(), num=1000)
            x_cycle_linspace = np.linspace(x_cycle_axis.min(), x_cycle_axis.max(), num=1000)

        f_throughput = interpolate.interp1d(x_throughput_axis, y_interpolation_axis, kind='linear',
                                            bounds_error=bounds_error, fill_value=fill_value)
        f_cycle = interpolate.interp1d(x_cycle_axis, y_interpolation_axis, kind='linear', bounds_error=bounds_error,
                                       fill_value=fill_value)

        throughput_crossing_array = abs(f_throughput(x_throughput_linspace) - threshold)
        cycle_crossing_array = abs(f_cycle(x_cycle_linspace) - threshold)
        throughput_to_threshold = x_throughput_linspace[np.argmin(throughput_crossing_array)]
        cycles_to_threshold = x_cycle_linspace[np.argmin(cycle_crossing_array)]

        if ~(throughput_to_threshold > 0) or ~(cycles_to_threshold > 0):
            print(run, " does not have a positive value to threshold")
            continue

        real_throughput_to_threshold = throughput_to_threshold * run_target_df['initial_regular_throughput'].values[0]

        threshold_dict = {
            "file": [run],
            "seq_num": [int(run.split("_")[1])],
            'initial_regular_throughput': run_target_df['initial_regular_throughput'].values[0],
            cycle_type + metric + str(threshold) + "_normalized_reg_throughput": [throughput_to_threshold],
            cycle_type + metric + str(threshold) + "_real_reg_throughput": [real_throughput_to_threshold],
            cycle_type + metric + str(threshold) + "_cycles": [cycles_to_threshold]
        }

        threshold_values_df_list.append(pd.DataFrame(threshold_dict))
    threshold_targets_df = pd.concat(threshold_values_df_list)
    threshold_targets_df.reset_index(drop=True, inplace=True)
    return threshold_targets_df


def get_parameter_dict(file_list, parameters_path):
    """
    Helper function to generate a dictionary with

    Args:
        file_list (list): List of filenames from self.filenames
        parameters_path (str): Root directory storing project parameter files.

    Returns:
        Dictionary with file_list as keys, and corresponding dictionary of protocol parameters as values
    """
    d = {}  # dict allows combining two different project parameter sets into the same structure
    for file in file_list:
        param_row, _ = parameters_lookup.get_protocol_parameters(file, parameters_path)
        d[file] = param_row.to_dict('records')[0]  # to_dict('records') returns a list.
    return d
