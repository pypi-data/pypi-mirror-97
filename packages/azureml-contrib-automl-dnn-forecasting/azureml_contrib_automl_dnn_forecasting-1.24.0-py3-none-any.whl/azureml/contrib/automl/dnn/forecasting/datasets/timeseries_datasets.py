# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for creating training dataset from dapaprep Dataflow object."""
import math
from typing import Any, List

import forecast.data.transforms as tfs
import numpy as np
import pandas as pd
import torch
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty
from forecast.data import FUTURE_DEP_KEY, FUTURE_IND_KEY, PAST_DEP_KEY, PAST_IND_KEY
from forecast.data.sources.data_source import DataSourceConfig
from forecast.data.sources.data_source import EncodingSpec
from torch.utils.data import Dataset

from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared._diagnostics.automl_error_definitions import TimeseriesNothingToPredict, \
    ForecastHorizonExceeded
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import ConfigException, DataException, ValidationException
from azureml.automl.runtime import _ml_engine as ml_engine
from azureml.automl.runtime.column_purpose_detection import ColumnPurposeDetector
import azureml.automl.runtime.featurizer.transformer.timeseries as automl_transformer

from ..constants import FeatureType, ForecastConstant, DROP_COLUMN_LIST
from ..types import DataInputType, TargetInputType


class _DataGrainItem:
    """This class holds a slice of feature and label."""

    def __init__(self,
                 X: np.ndarray,
                 y: np.ndarray,
                 lookup_start_ix: int = 0,
                 lookup_end_ix: int = None,
                 offset: int = 0):
        self.X = X
        self.y = y
        self.lookup_start_ix = lookup_start_ix
        self.lookup_end_ix = lookup_end_ix
        self.offset = offset

        Contract.assert_true(X.shape[-1] == y.shape[-1],
                             "X({}) and y({}) have inconsistent shapes.".format(X.shape[-1], y.shape[-1]),
                             log_safe=True)

        if lookup_end_ix:
            Contract.assert_true(lookup_end_ix > lookup_start_ix,
                                 "lookup_end_ix ({}) should be greater than lookup_start_ix ({})".format(
                                     lookup_end_ix, lookup_start_ix), log_safe=True)


# Copied here temporarily, it will be imported from automl.client.core.runner.model_wrappers.
class ForecastingErrors:
    """Forecasting errors."""

    # Constants for errors and warnings
    # Non recoverable errors.
    FATAL_WRONG_DESTINATION_TYPE = ("The forecast_destination argument has wrong type, "
                                    "it is a {}. We expected a datetime.")
    FATAL_DATA_SIZE_MISMATCH = "The length of y_pred is different from the X_pred"
    FATAL_WRONG_X_TYPE = ("X_pred has unsupported type, x should be pandas.DataFrame, "
                          "but it is a {}.")
    FATAL_WRONG_Y_TYPE = ("y_pred has unsupported type, y should be numpy.array or pandas.DataFrame, "
                          "but it is a {}.")
    FATAL_NO_DATA_CONTEXT = ("No y values were provided for one of grains. "
                             "We expected non-null target values as prediction context because there "
                             "is a gap between train and test and the forecaster "
                             "depends on previous values of target. ")
    FATAL_NO_DESTINATION_OR_X_PRED = ("Input prediction data X_pred and forecast_destination are both None. " +
                                      "Please provide either X_pred or a forecast_destination date, but not both.")
    FATAL_DESTINATION_AND_X_PRED = ("Input prediction data X_pred and forecast_destination are both set. " +
                                    "Please provide either X_pred or a forecast_destination date, but not both.")
    FATAL_X_Y_XOR = "X_pred and y_pred should both be None or both not None."
    FATAL_NO_LAST_DATE = ("The last training date was not provided."
                          "One of grains in scoring set was not present in training set.")
    FATAL_EARLY_DESTINATION = ("Input prediction data X_pred or input forecast_destination contains dates " +
                               "prior to the latest date in the training data. " +
                               "Please remove prediction rows with datetimes in the training date range " +
                               "or adjust the forecast_destination date.")
    FATAL_NO_TARGET_IN_Y_DF = ("The y_pred is a data frame, "
                               "but it does not contain the target value column")
    FATAL_WRONG_QUANTILE = "Quantile should be a number between 0 and 1 (not inclusive)."
    FATAL_NO_TS_TRANSFORM = ("The time series transform is absent. "
                             "Please try training model again.")

    FATAL_NO_GRAIN_IN_TRAIN = ("One of grains was not present in the training data set. "
                               "Please remove it from the prediction data set to proceed.")
    FATAL_NO_TARGET_IMPUTER = 'No target imputers were found in TimeSeriesTransformer.'
    FATAL_NONPOSITIVE_HORIZON = "Forecast horizon must be a positive integer."


class AbstractDNNTimeSeriesDataset(Dataset):
    """This abstract class provides a base class for Time Series datasets."""

    @staticmethod
    def _drop_extra_columns(X: pd.DataFrame) -> pd.DataFrame:
        drop_columns = []
        for col in X.columns:
            if col in DROP_COLUMN_LIST:
                drop_columns.append(col)
        if drop_columns:
            return X.drop(drop_columns, inplace=False, axis=1)
        return X

    def __init__(self,
                 horizon: int,
                 lookback: int,
                 step: int = 1,
                 thinning: float = 1.0,
                 has_past_regressors: bool = False,
                 pre_transform: automl_transformer.TimeSeriesTransformer = None,
                 transform: Any = None,
                 fetch_y_only: bool = False,
                 training_data: tuple = None,
                 dset_config: DataSourceConfig = None,
                 data_grains: List[_DataGrainItem] = None):
        """
        Take a training data(X) and label(y) and provides access to windowed subseries for torch DNN training.

        :param horizon: Number of time steps to forecast.
        :param lookback: lookback for this class.
        :param step: Time step size between consecutive examples.
        :param thinning: Fraction of examples to include.
        :param has_past_regressors: data to populate past regressors for each sample
        :param pre_transform: pre_transformer to use
        :param transform: feature transforms to use
        :param fetch_y_only: Get only the target value.
        :param train_transform: whether training is needed for transformers
        :param training_data: X and Y and settings saved in dataset if needed to created lookback.
        :param dset_config: Get only the target value.
        :param data_grain: Slices of data grain and the indexes to lookup the training sample.
        """
        self.horizon = horizon
        self.step = step
        self.thinning = thinning
        self.transform = transform
        self._pre_transform = pre_transform
        self._keep_untransformed = False
        self.has_past_regressors = has_past_regressors
        self._len = None
        self.lookback = lookback
        self.fetch_y_only = fetch_y_only
        self._training_data = training_data
        self.dset_config = dset_config
        self._cache = {}
        self._data_grains = data_grains
        if self._pre_transform is not None:
            Contract.assert_type(self._pre_transform, "pre_transform", automl_transformer.TimeSeriesTransformer)
        self.cross_validation = None

    @property
    def keep_untransformed(self):
        """Whether to return data untransformed."""
        return self._keep_untransformed

    @property
    def pre_transform(self):
        """Pre transforms for this timeseries dataset."""
        return self._pre_transform


class TimeSeriesDataset(AbstractDNNTimeSeriesDataset):
    """This class provides a dataset for training timeseries model with dataprep features and label."""

    def __init__(self,
                 X_dflow: DataInputType,
                 y_dflow: TargetInputType,
                 horizon: int,
                 step: int = 1,
                 thinning: float = 1.0,
                 has_past_regressors: bool = False,
                 one_hot: bool = False,
                 pre_transform: automl_transformer.TimeSeriesTransformer = None,
                 transform: Any = None,
                 train_transform: bool = False,
                 fetch_y_only: bool = False,
                 save_last_lookback_data: bool = False,
                 **settings: Any):
        """
        Take a training data(X) and label(y) and provides access to windowed subseries for torch DNN training.

        :param X_dflow: Training features in DataPrep DataFlow form(numeric data of shape(row_count, feature_count).
        :param y_dflow: Training label in DataPrep DataFlow for with shape(row_count, 1).
        :param horizon: Number of time steps to forecast.
        :param step: Time step size between consecutive examples.
        :param thinning: Fraction of examples to include.
        :param has_past_regressors: data to populate past regressors for each sample
        :param one_hot: one_hot encode or not
        :param pre_transform: pre_transformer to use
        :param transform: feature transforms to use
        :param train_transform: whether training is needed for transformers
        :param settings: automl timeseries settings for pre_transform
        """
        AbstractDNNTimeSeriesDataset.__init__(self,
                                              horizon,
                                              None,
                                              step=step,
                                              thinning=thinning,
                                              has_past_regressors=has_past_regressors,
                                              pre_transform=pre_transform,
                                              transform=transform,
                                              fetch_y_only=fetch_y_only
                                              )
        if self._pre_transform is not None:
            assert isinstance(self._pre_transform, automl_transformer.TimeSeriesTransformer)
        if isinstance(X_dflow, pd.DataFrame):
            X_df = X_dflow
        else:
            X_df = X_dflow.to_pandas_dataframe(extended_types=True)

        if isinstance(y_dflow, np.ndarray) or isinstance(y_dflow, pd.Series):
            y_df = pd.DataFrame(y_dflow)
        elif isinstance(y_dflow, pd.DataFrame):
            y_df = y_dflow
        else:
            y_df = y_dflow.to_pandas_dataframe(extended_types=True)
        if save_last_lookback_data:
            self._training_data = (X_df, y_df, settings)

        if isinstance(horizon, str):
            settings[ForecastConstant.Horizon] = ForecastConstant.auto
        get_encodings, encodings = False, []
        if ForecastConstant.cross_validations in settings and settings[ForecastConstant.cross_validations] is not None:
            self.cross_validation = int(settings[ForecastConstant.cross_validations])
        if train_transform and self._pre_transform is None and settings is not None and len(settings) > 0:
            # Create a timeseries transform which is applied before data is passed to DNN
            feat_config = FeaturizationConfig()
            if settings.get("featurization_config"):
                feat_config = settings.get("featurization_config")
                del settings["featurization_config"]
            (
                forecasting_pipeline,
                ts_param_dict,
                lookback_removed,
                time_index_non_holiday_features
            ) = ml_engine.suggest_featurizers_timeseries(
                X_df,
                y_df,
                feat_config,
                settings,
                automl_transformer.TimeSeriesPipelineType.FULL
            )

            self._pre_transform = automl_transformer.TimeSeriesTransformer(
                forecasting_pipeline,
                automl_transformer.TimeSeriesPipelineType.FULL,
                feat_config,
                time_index_non_holiday_features,
                lookback_removed,
                **ts_param_dict
            )
            self._pre_transform.fit(X_df, y_df)
            if one_hot:
                get_encodings = True

        if self._pre_transform:
            X_transformed = self._pre_transform.transform(X_df, y_df)
            X_transformed = X_transformed.sort_index(axis=0)
            if ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN in X_transformed:
                y_df = X_transformed[ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN]
            X_transformed = self._drop_extra_columns(X_transformed)
        else:
            X_transformed = X_df

        if isinstance(horizon, str) and self._pre_transform is not None:
            horizon = self._pre_transform.max_horizon
            self.horizon = horizon

        if get_encodings:
            encodings = self._get_embedding(X_transformed)

        self.dset_config = DataSourceConfig(feature_channels=X_transformed.shape[1],
                                            forecast_channels=1,
                                            encodings=encodings)

        self._data_grains = []
        grains = settings.get(ForecastConstant.grain_column_names, None) if settings else None
        if grains is not None:
            if isinstance(grains, str):
                grains = [grains]
            assert ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN not in X_transformed
            X_transformed.insert(0, ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN,
                                 y_df.values)
            groupby = X_transformed.groupby(grains)
            for grain in groupby.groups:
                X_df = groupby.get_group(grain)
                y_df = X_df[ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN]
                X = X_df.values.T
                y = y_df.values
                y = y.reshape((1, y.shape[0]))
                self._data_grains.append(_DataGrainItem(X, y))
        else:
            X = X_transformed.values.T
            y = y_df.values
            y = y.reshape((1, y.shape[0]))
            X = np.vstack((y, X))
            self._data_grains.append(_DataGrainItem(X, y))

        self.has_past_regressors = has_past_regressors
        if self.transform is None and not self.fetch_y_only:
            self.transform = self._get_transforms(one_hot)

    def set_lookback(self, lookback: int) -> None:
        """
        Set lookback to be used with this dataset.

        :param lookback: Number of time steps used as input for forecasting.
        """
        self.lookback = lookback
        self._len = 0
        for item in self._data_grains:
            start_index = self._len
            size = self._get_size(item.y)
            self._len += size
            item.lookup_start_ix = start_index
            item.lookup_end_ix = self._len

    def get_last_lookback_items(self) -> pd.DataFrame:
        """Return the lookback items from each grain in dataset."""
        if not self._training_data:
            raise ConfigException._with_error(
                AzureMLError.create(ArgumentBlankOrEmpty, target="save_data", argument_name="X_dflow/y_dflow/settings")
            )
        if self.lookback is None:
            raise ConfigException._with_error(
                AzureMLError.create(ArgumentBlankOrEmpty, target="lookback", argument_name="lookback")
            )
        X_df, y_df, settings = self._training_data
        if settings is None:
            raise ConfigException._with_error(
                AzureMLError.create(ArgumentBlankOrEmpty, target="time_column", argument_name="settings")
            )
        X_df = X_df.copy()
        y_df = y_df.copy()
        grains, index = None, None
        assert ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN not in X_df
        X_df[ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_df.values
        if ForecastConstant.automl_constants.TimeSeries.TIME_COLUMN_NAME in settings:
            index = settings[ForecastConstant.automl_constants.TimeSeries.TIME_COLUMN_NAME]
            if ForecastConstant.automl_constants.TimeSeries.GRAIN_COLUMN_NAMES in settings:
                grains = settings[ForecastConstant.automl_constants.TimeSeries.GRAIN_COLUMN_NAMES]
        if index is None:
            ret_df = X_df[-self.lookback:]
        else:
            X_indexed = X_df.set_index(index)
            X_indexed = X_df.sort_index(axis=0)
            if grains:
                ret_df = X_indexed[0:0].reset_index()
                groupby = X_df.groupby(grains)
                for grain in groupby.groups:
                    X_df = groupby.get_group(grain)
                    ret_df = ret_df.append(X_df[-self.lookback:].reset_index())
            else:
                ret_df = X_df[self.lookback:].reset_index()
        return ret_df[X_df.columns]

    def _get_size(self, y) -> None:
        """
        Set lookback to be used with this dataset.

        :param lookback: Number of time steps used as input for forecasting.
        """
        # If timeseries is smaller than lookback + horizon, we would need to pad
        if y.shape[-1] < self.lookback + self.horizon:
            sample_count = 1
        else:
            sample_count = (y.shape[-1] - self.lookback - self.horizon + self.step) // self.step
        return max(1, int(self.thinning * sample_count))

    def is_small_dataset(self) -> bool:
        """Return true if dataset is small."""
        if self._len is not None:
            return self._len < ForecastConstant.SMALL_DATASET_MAX_ROWS
        return True

    @staticmethod
    def _get_embedding(data: pd.DataFrame) -> List[EncodingSpec]:
        index = 0
        encodings = []
        column_purpose_detector = ColumnPurposeDetector()
        column_purpose = column_purpose_detector.get_raw_stats_and_column_purposes(data)
        for stats, featureType, name in column_purpose:
            if featureType == FeatureType.Categorical and stats.num_unique_vals > 2:
                # TODO remove this and replace this with label encoder
                max_num_features = int(data[name].max().astype(int) + 1)
                # embedding = EncodingSpec(feature_index=index, num_vals=stats.num_unique_vals)
                embedding = EncodingSpec(feature_index=index, num_vals=max_num_features)
                encodings.append(embedding)
            index = index + 1
        return encodings

    def _get_transforms(self, one_hot) -> tfs.ComposedTransform:
        targets = [0]
        tf_list = [
            tfs.LogTransform(offset=1.0, targets=targets),
            tfs.SubtractOffset(targets=targets)
        ]
        drop_first = False
        if one_hot and self.dset_config.encodings:
            drop = True if drop_first else False
            tf_list = [tfs.OneHotEncode([e.feature_index for e in self.dset_config.encodings],
                                        [e.num_vals for e in self.dset_config.encodings],
                                        drop_first=drop),
                       tfs.OneHotEncode([e.feature_index for e in self.dset_config.encodings],
                                        [e.num_vals for e in self.dset_config.encodings],
                                        drop_first=drop,
                                        key=FUTURE_IND_KEY)] + tf_list
        return tfs.ComposedTransform(tf_list)

    def __len__(self) -> int:
        """Return the number of samples in the dataset.

        :return: number of samples.
        """
        return self._len

    def feature_count(self):
        """Return the number of features in the dataset."""
        return self._data_grains[0].X.shape[0]

    def _get_test_size(self, grain_size, validation_percent):
        if self.cross_validation is not None:
            grain_test_size = self.cross_validation * self.horizon
            if grain_test_size >= grain_size:
                grain_test_size = 0
        else:
            grain_test_size = max(1, math.floor(grain_size * validation_percent))
            if grain_size == grain_test_size:
                grain_test_size = 0
        return grain_test_size

    def get_train_test_split(self, validation_percent: float = 0.1):
        """
        Split the dataset into train and test as per the validtaion percent.

        :param validation_percent: percentage of data to be used as validation.
        """
        if self.lookback is None:
            raise ConfigException._with_error(
                AzureMLError.create(ArgumentBlankOrEmpty, target="lookback", argument_name="lookback")
            )
        train_size = 0
        test_size = 0
        test_data_grains = []
        train_data_grains = []
        for item in self._data_grains:
            # total samples in the grain.
            grain_size = item.lookup_end_ix - item.lookup_start_ix
            grain_test_size = self._get_test_size(grain_size, validation_percent)
            grain_train_size = grain_size - grain_test_size
            train_item = _DataGrainItem(item.X, item.y, train_size, train_size + grain_train_size)
            train_size += grain_train_size
            train_data_grains.append(train_item)
            if grain_test_size > 0:
                grain_test_size = math.ceil(grain_test_size / self.horizon)
                test_item = _DataGrainItem(item.X, item.y, test_size, test_size + grain_test_size, grain_train_size)
                test_size += grain_test_size
                test_data_grains.append(test_item)

        train_dataset = TransformedTimeSeriesDataset(train_data_grains, self.horizon, self.lookback, train_size,
                                                     self.dset_config, self.step, self.has_past_regressors,
                                                     self.pre_transform, self.transform, self.fetch_y_only)

        test_dataset = TransformedTimeSeriesDataset(test_data_grains, self.horizon, self.lookback, test_size,
                                                    self.dset_config, self.horizon, self.has_past_regressors,
                                                    self.pre_transform, self.transform, self.fetch_y_only)
        assert len(test_data_grains) <= len(train_data_grains)
        if len(test_data_grains) == 0:
            msg = "length of test grain {0}, train size = {1}".\
                format(len(test_data_grains), len(train_data_grains))
            assert len(test_data_grains) > 0, msg

        return train_dataset, test_dataset

    def __getitem__(self, idx: int) -> dict:
        """
        Get the idx-th training sample item from the dataset.

        :param idx: the item to get the sample.
        :return: returns the idx-th sample.
        """
        idx2, X, y = self._get_index_grain_from_lookup(idx)
        sample = self. _getitem_from_df(X, y, idx2)
        return sample

    def _get_index_grain_from_lookup(self, idx) -> tuple:
        located_grain = None
        for item in self._data_grains:
            if idx >= item.lookup_start_ix and idx < item.lookup_end_ix:
                located_grain = item
                break

        if located_grain is None:
            raise ValidationException._with_error(AzureMLError.create(
                ArgumentBlankOrEmpty, argument_name="located_grain ({})".format(idx), target="located_grain")
            )

        # lookup index from the grain is the offset +
        # steps size * distance to the index from lookup start.
        lookup_index = located_grain.offset + self.step * (idx - located_grain.lookup_start_ix)
        return lookup_index, located_grain.X, located_grain.y

    def _getitem_from_df(self, X, y, idx: int) -> dict:
        """
        Get the idx-th training sample item from the dataset.

        :param X: feature ndarray
        :param y: target array
        :param idx: the item to get the sample.
        :return: returns the idx-th sample.
        """
        # Get time series
        # The data values are transformed so the result is of the shape nfeatures X lookback for X
        # and 1 X horizon for y
        start_index = idx
        X_past = None
        X_fut = None
        if self.has_past_regressors:
            if X.shape[-1] < self.lookback + self.horizon:
                # If the time series is too short, zero-pad on the left
                if not self.fetch_y_only:
                    X_past = X[1:, :-self.horizon]
                    X_past = np.pad(
                        X_past,
                        pad_width=((0, 0), (self.lookback - X_past.shape[-1], 0)),
                        mode='constant',
                        constant_values=0
                    )
                    X_fut = X[1:, -self.horizon:]

                    X_past = torch.tensor(X_past.astype(np.float32), dtype=torch.float)
                    X_fut = torch.tensor(X_fut.astype(np.float32), dtype=torch.float)

                y_past = y[:, :-self.horizon]
                y_past = np.pad(
                    y_past,
                    pad_width=((0, 0), (self.lookback - y_past.shape[-1], 0)),
                    mode='constant',
                    constant_values=0
                )
                y_fut = y[:, -self.horizon:]

                y_past = torch.tensor(y_past.astype(np.float32), dtype=torch.float)
                y_fut = torch.tensor(y_fut.astype(np.float32), dtype=torch.float)
            else:
                end_index = start_index + self.lookback + self.horizon
                if not self.fetch_y_only:
                    X_item = X[1:, start_index:end_index]
                    X_past = torch.tensor(X_item[:, :self.lookback].astype(np.float32), dtype=torch.float)
                    X_fut = torch.tensor(X_item[:, self.lookback:].astype(np.float32), dtype=torch.float)
                y_item = y[:, start_index:end_index]
                y_past = torch.tensor(y_item[:, :self.lookback].astype(np.float32), dtype=torch.float)
                y_fut = torch.tensor(y_item[:, self.lookback:].astype(np.float32), dtype=torch.float)

            # Create the input and output for the sample
            if self.fetch_y_only:
                sample = {PAST_DEP_KEY: y_past,
                          FUTURE_DEP_KEY: y_fut}
            else:
                sample = {PAST_IND_KEY: X_past,
                          PAST_DEP_KEY: y_past,
                          FUTURE_IND_KEY: X_fut,
                          FUTURE_DEP_KEY: y_fut}
        else:
            X = None
            if not self.fetch_y_only:
                X_item = X[:, start_index:start_index + self.lookback]
                X = torch.tensor(X_item.astype(np.float32), dtype=torch.float)
            y_item = y[:, start_index + self.lookback:start_index + self.lookback + self.horizon]
            y = torch.tensor(y_item.astype(np.float32), dtype=torch.float)
            # Create the input and output for the sample
            sample = {'X': X, 'y': y}
        if self.transform and not self.keep_untransformed:
            sample = self.transform(sample)
        return sample


class TransformedTimeSeriesDataset(TimeSeriesDataset):
    """This class provides a dataset for based on automl transformed data and used in train test split."""

    def __init__(self, data_grains: List[_DataGrainItem],
                 horizon: int,
                 lookback: int,
                 len: int,
                 dset_config: DataSourceConfig,
                 step: int = 1,
                 has_past_regressors: bool = False,
                 pre_transform: automl_transformer.TimeSeriesTransformer = None,
                 transform: Any = None,
                 fetch_y_only: bool = False):
        """
        Take a list of grains amd and provides access to windowed subseries for torch DNN training.

        :param data_grains : list of datagrains.
        :param horizon: Number of time steps to forecast.
        :param lookback: look back to use with in examples.
        :param len: number of samples in the grains.
        :param step: Time step size between consecutive examples.
        :param dset_config: dataset config
        :param has_past_regressors: data to populate past regressors for each sample
        :param pre_transform: pre_transformer to use
        :param transform: feature transforms to use
        :param fetch_y_only: whether fetch_y_only
        """
        AbstractDNNTimeSeriesDataset.__init__(self,
                                              horizon,
                                              lookback,
                                              step=step,
                                              has_past_regressors=has_past_regressors,
                                              pre_transform=pre_transform,
                                              transform=transform,
                                              fetch_y_only=fetch_y_only,
                                              data_grains=data_grains,
                                              dset_config=dset_config)
        self._len = len


class TimeSeriesInferenceDataset(TimeSeriesDataset):
    """This class provides a dataset for training timeseries model with dataprep features and label."""

    def __init__(self,
                 X_dflow: DataInputType,
                 y_dflow: TargetInputType,
                 saved_data: pd.DataFrame,
                 horizon: int,
                 lookback: int,
                 dset_config: DataSourceConfig,
                 has_past_regressors: bool = False,
                 pre_transform: automl_transformer.TimeSeriesTransformer = None,
                 transform: Any = None,
                 **settings: Any):
        """
        Take a inference data(X) and label(y) and provide the last item from each grain.

        :param X_dflow: Training features in DataPrep DataFlow form(numeric data of shape(row_count, feature_count).
        :param y_dflow: Training label in DataPrep DataFlow for with shape(row_count, 1).
        :param saved_data: Pandas Dataframe of last look back items from training data.
        :param horizon: Number of time steps to forecast.
        :param lookback: lookback for the model.
        :param dset_config: dataset settings
        :param has_past_regressors: data to populate past regressors for each sample
        :param pre_transform: pre_transformer to use
        :param transform: feature transforms to use
        :param settings: automl timeseries settings for pre_transform
        """
        AbstractDNNTimeSeriesDataset.__init__(self,
                                              horizon,
                                              lookback,
                                              step=1,
                                              has_past_regressors=has_past_regressors,
                                              pre_transform=pre_transform,
                                              transform=transform,
                                              fetch_y_only=False,
                                              dset_config=dset_config)

        dummy_target_column = ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
        if isinstance(X_dflow, pd.DataFrame):
            X_df = X_dflow
        else:
            X_df = X_dflow.to_pandas_dataframe(extended_types=True)

        if isinstance(y_dflow, np.ndarray) or isinstance(y_dflow, pd.Series):
            y_df = pd.DataFrame(y_dflow)
        elif isinstance(y_dflow, pd.DataFrame):
            y_df = y_dflow
        else:
            y_df = y_dflow.to_pandas_dataframe(extended_types=True)
        X_df = X_df.copy()
        y_df = y_df.copy()

        time_column = settings[ForecastConstant.time_column_name]
        target_column = ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
        X_df[target_column] = y_df.values
        self._X_orig = X_df.copy()
        if saved_data is not None:
            saved_indexed = saved_data.set_index(time_column)

        grains = None
        if ForecastConstant.automl_constants.TimeSeries.GRAIN_COLUMN_NAMES in settings:
            grains = settings[ForecastConstant.automl_constants.TimeSeries.GRAIN_COLUMN_NAMES]
        if grains is None:
            if X_df.shape[0] < self.lookback + self.horizon:
                min_time_value = min(X_df[time_column])
                X_df = X_df.append(saved_indexed[saved_indexed.index < min_time_value].reset_index()[X_df.columns])
                self._check_required_prediction_horizon(X_df, horizon, time_column, target_column)
            self._len = 1
        else:
            Xdf_indexed = X_df.set_index(time_column)
            Xdf_indexed = Xdf_indexed.sort_index(axis=0)
            Xdf_grains = Xdf_indexed.groupby(grains)
            saved_grains = saved_indexed.groupby(grains)
            grain_keys = Xdf_grains.groups.keys()
            saved_keys = saved_grains.groups.keys()
            self._len = 0
            for grain_key in grain_keys:
                self._len += 1
                grain_item = Xdf_grains.get_group(grain_key)
                self._check_required_prediction_horizon(grain_item.reset_index(), horizon, time_column, target_column)
                if grain_key in saved_keys:
                    if grain_item.shape[0] < self.lookback + self.horizon:
                        saved_item = saved_grains.get_group(grain_key)
                        min_time_value = min(grain_item.reset_index()[time_column])
                        X_df = X_df.append(saved_item[saved_item.index < min_time_value].reset_index()[X_df.columns])
        y_df = X_df.pop(ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN)
        X_transformed = X_df
        if self.pre_transform:
            X_transformed = self._pre_transform.transform(X_df, y_df.values)
            X_transformed = X_transformed.sort_index(axis=0)
            y_df = X_transformed[dummy_target_column]
            X_transformed = self._drop_extra_columns(X_transformed)
        self._data_grains = []
        self._data_frames = []
        if dummy_target_column not in X_transformed.columns:
            X_transformed.insert(0, dummy_target_column, y_df.values)

        count_per_grain_needed = self.lookback + self.horizon
        index_columns = [time_column]
        if grains is None:
            y_item = y_df
            # set the index to last item.
            X_item = X_transformed[-(count_per_grain_needed):]
            y_item = y_item[-(count_per_grain_needed):]
            self._data_frames.append({"X": X_item, "y": y_item})

            self._data_grains.append(_DataGrainItem(X_item.values.T,
                                                    y_item.values.reshape(1, y_item.shape[0]),
                                                    0,
                                                    1,
                                                    0))
        else:
            index_columns.extend(grains)
            offset = 0
            X_transformed_grains = X_transformed.groupby(grains)
            transformed_grain_keys = X_transformed_grains.groups.keys()
            for grain_key in transformed_grain_keys:
                X_item = X_transformed_grains.get_group(grain_key)
                y_item = X_item[dummy_target_column]
                X_item = X_item[-(count_per_grain_needed):]
                y_item = y_item[-(count_per_grain_needed):]
                self._data_frames.append({"X": X_item, "y": y_item})
                self._data_grains.append(_DataGrainItem(X_item.values.T,
                                                        y_item.values.reshape(1, y_item.shape[0]),
                                                        offset,
                                                        offset + 1,
                                                        0))
                offset += 1

        # try to convert the time column to datatime
        if self._X_orig.dtypes[time_column] != np.dtype('datetime64[ns]'):
            try:
                self._X_orig[time_column] = pd.to_datetime(self._X_orig[time_column])
            except ValueError:
                pass
        self._X_orig.set_index(index_columns)
        self._index_columns = index_columns

    @staticmethod
    def _check_required_prediction_horizon(X_df, horizon, time_column, target_column):
        if np.any(np.isnan(X_df[target_column])):
            forecast_origin = min(X_df[X_df[target_column] is None or np.isnan(X_df[target_column])][time_column])
        else:
            raise DataException._with_error(AzureMLError.create(TimeseriesNothingToPredict))
        if X_df[X_df[time_column] >= forecast_origin].shape[0] > horizon:
            raise DataException._with_error(AzureMLError.create(ForecastHorizonExceeded, target="horizon"))

    def merge_results(self, y_pred: np.ndarray):
        """
        Get the idx-th training sample item from the dataset.

        :param X: feature ndarray
        :param y: target array
        :param idx: the item to get the sample.
        :return: returns the idx-th sample.
        """
        result = self._data_frames[0]['X'][0:0]
        target_column_name = ForecastConstant.automl_constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN
        for i, item in enumerate(self._data_frames):
            X = item['X'].copy()
            X[target_column_name][-self.horizon:] = y_pred[0][i].reshape(-1)
            result = result.append(X)
        if len(self._index_columns) == 1:  # no grains
            result = result.reset_index().set_index(self._index_columns)

        left, right = '_orig', '_pred'
        X_orig = self._X_orig.copy()
        merged = X_orig.join(result, on=self._index_columns, how='left', lsuffix=left, rsuffix=right)
        left_name = "{0}{1}".format(target_column_name, left)
        right_name = "{0}{1}".format(target_column_name, right)
        X_orig[target_column_name] = np.where(np.isnan(merged[left_name]), merged[right_name], merged[left_name])
        return X_orig.set_index(self._index_columns)
