"""This module provides utilities for driving model training."""

import dataclasses as dc
from typing import Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from tqdm import tqdm

from forecast.callbacks import Callback, CallbackList, MetricCallback
from forecast.data import FUTURE_DEP_KEY, FUTURE_IND_KEY, PAST_DEP_KEY, PAST_IND_KEY
from forecast.data.transforms import AbstractTransform, unbatch_and_undo
from forecast.metrics import Metric
from forecast.models import ForecastingModel
from forecast.utils import EarlyTerminationException


@dc.dataclass
class TorchResults:
    """A container for passing the results of one or more predictions which leverages `torch.Tensor`s."""

    loss: float
    predictions: List[torch.Tensor]


def _to(x: torch.Tensor, device: str) -> Optional[torch.Tensor]:
    return x.to(device, non_blocking=True) if x is not None else None


class Forecaster:
    """An optional utility for driving a training run of a model."""

    def __init__(self,
                 model: ForecastingModel,
                 device: str = 'cuda',
                 metrics: Optional[Union[Metric, Sequence[Metric], Mapping[str, Metric]]] = None,
                 callbacks: Optional[Union[Callback, Sequence[Callback]]] = None):
        """An optional utility for driving a training run of a model.

        Parameters
        ----------
        model: ForecastingModel
            The model to train
        device: str, optional
            The device on which training should occur, defaults to 'cuda'
        metrics: Union[Metric, Sequence[Metric], Mapping[str, Metric]], optional
            Metrics to compute for each epoch. Defaults to None.
        callbacks: Union[Callback, Sequence[Callback]], optional
            Callbacks to execute during training and inference. Defaults to None.

        """
        # place model and loss on device
        self.device = device if torch.cuda.is_available() and 'cuda' in device else 'cpu'
        self.model = model.to(device)

        # only used in training
        self.loss: Optional[nn.Module] = None
        self.optimizer: Optional[Optimizer] = None

        # populate our metrics dictionaries
        self._train_metrics: Dict[str, Metric] = {}
        self._val_metrics: Dict[str, Metric] = {}
        if metrics:
            self._add_metrics(metrics)

        # ensure MetricCallback is first as it will populate our train/val metrics
        # this callback correctly handles the case when both sets of metrics are empty dicts
        #
        # Note: this callback stores a reference to self._train_metrics and self._val_metrics. as such, any change to
        # either is automatically reflected in the MetricCallback. it also means that these objects must be modified
        # IN-PLACE (!!!) to ensure proper functionality.
        cb_list: List[Callback] = [MetricCallback(self._train_metrics, self._val_metrics)]
        if isinstance(callbacks, Callback):
            cb_list += [callbacks]
        elif isinstance(callbacks, Sequence):
            cb_list += list(callbacks)
        elif callbacks is not None:
            raise TypeError(f'Invalid type for parameter `callbacks`: {type(callbacks)}')

        # set out callbacks
        self._callbacks = CallbackList(cb_list, self.model)

    def _add_metrics(self, metrics: Union[Metric, Sequence[Metric], Mapping[str, Metric]]) -> None:
        """Adds one or more metrics to be computed.

        Parameters:
        -----------
        metrics: Union[Metric, Sequence[Metric], Mapping[str, Metric]], optional
            Metrics to compute for each epoch. Defaults to None.

        Returns:
        --------
        None

        """
        if isinstance(metrics, Metric):
            metrics = [metrics]  # if a single metric is provided, convert to a list & fall through to later cases
        if isinstance(metrics, Sequence):
            for metric in metrics:
                if metric.computed_on_train:
                    if metric.__class__.__name__ in self._train_metrics:
                        raise ValueError(f'More than one training `Metric` with name "{metric.__class__.__name__}"'
                                         ' supplied. Please supply a Mapping instead of Sequence to prevent a name'
                                         ' collision.')
                    self._train_metrics[metric.__class__.__name__] = metric
                if metric.computed_on_val:
                    if metric.__class__.__name__ in self._val_metrics:
                        raise ValueError(f'More than one val `Metric` with name "{metric.__class__.__name__}"'
                                         ' supplied. Please supply a Mapping instead of Sequence to prevent a name'
                                         ' collision.')
                    self._val_metrics[metric.__class__.__name__] = metric
        elif isinstance(metrics, Mapping):
            for name, metric in metrics.items():
                if metric.computed_on_train:
                    self._train_metrics[name] = metric
                if metric.computed_on_val:
                    self._val_metrics[name] = metric
        else:
            raise TypeError(f'Invalid type for parameter `metrics`: {type(metrics)}')

    def fit(self,
            dataloader_train: DataLoader,
            loss: nn.Module,
            optimizer: Optimizer,
            epochs: int,
            dataloader_val: Optional[DataLoader] = None) -> None:
        """Trains a model given and optionally evaluates it on a validation set.

        Parameters
        ----------
        dataloader_train: torch.utils.data.DataLoader
            A torch DataLoader providing the training data
        loss: torch.nn.Module
            The loss function to apply
        optimizer: Optimizer
            The optimizer to drive model training
        epochs: int
            Number of epochs to execute
        dataloader_val: torch.utils.data.DataLoader
            A torch DataLoader providing the validation data

        Returns
        -------
        None

        """
        self._callbacks.on_train_begin()
        self.loss = loss.to(self.device)
        self.optimizer = optimizer

        for epoch in tqdm(range(epochs), desc='Job: ', dynamic_ncols=True):
            try:
                self._callbacks.on_train_epoch_begin(epoch)

                train_loss = self._train_epoch(dataloader_train, epoch)

                metrics: Dict[str, float] = {}
                self._callbacks.on_train_epoch_end(epoch, train_loss, metrics)

                # if validation dataloader, compute and log
                if dataloader_val:
                    self._callbacks.on_val_begin(epoch)

                    val_loss = self._evaluate(dataloader_val, epoch)

                    metrics = {}
                    self._callbacks.on_val_end(epoch, val_loss, metrics)

                self._callbacks.on_train_val_epoch_end(epoch)
            except EarlyTerminationException:
                break

        self._callbacks.on_train_end()

    def predict(self, dataloader: DataLoader) -> List[np.ndarray]:
        """Performs inference on the data contained in the dataloader.

        Parameters
        ----------
        dataloader: DataLoader
            The data on which inference should be performed

        Returns
        -------
        List[np.ndarray]
            Each element of the list corresponds to one of the model's forecast heads. The `np.ndarray` is of shape
            [N_batch * batch_size, forecast_horizon].

        """
        self._callbacks.on_predict_begin()

        # place the model in eval mode
        prev_model_train = self.model.training
        self.model.eval()

        tf: Optional[AbstractTransform] = dataloader.dataset.transform
        all_preds = []
        with torch.no_grad():
            for batch_ind, batch in enumerate(dataloader):
                self._callbacks.on_predict_batch_begin(batch_ind)

                # send batch to device
                X_past = _to(batch[PAST_IND_KEY], self.device)
                y_past = _to(batch[PAST_DEP_KEY], self.device)
                X_fut = _to(batch[FUTURE_IND_KEY], self.device)
                assert y_past is not None

                # compute the predictions/loss
                predictions = [p.to('cpu', non_blocking=True) for p in self.predict_batch(X_past, y_past, X_fut)]

                utf_preds = []
                for pred in predictions:
                    utf_preds.append(
                        np.concatenate([p[FUTURE_DEP_KEY] for p in unbatch_and_undo(batch, tf, pred)], axis=0)
                    )
                all_preds.append(utf_preds)
                self._callbacks.on_predict_batch_end(batch_ind)

        out = []
        for batch_pred in zip(*all_preds):
            out.append(np.concatenate(batch_pred, axis=0))

        # return the model to train mode if necessary
        if prev_model_train:
            self.model.train()

        self._callbacks.on_predict_end()
        return out

    def _train_epoch(self, dataloader: DataLoader, epoch: int) -> float:
        """Perform training for one epoch.

        Parameters
        ----------
        dataloader: torch.utils.data.DataLoader
            A torch DataLoader providing the training data
        epoch: int
            The epoch number

        Returns
        -------
        float
            The mean per-batch loss for the epoch

        """
        tot_loss = 0.
        tf = dataloader.dataset.transform

        for batch_ind, batch in enumerate(tqdm(dataloader, desc=f'Epoch {epoch}: ', leave=False, dynamic_ncols=True)):
            self._callbacks.on_train_batch_begin(epoch, batch_ind)

            # Send batch to device
            X_past = _to(batch[PAST_IND_KEY], self.device)
            y_past = _to(batch[PAST_DEP_KEY], self.device)
            X_fut = _to(batch[FUTURE_IND_KEY], self.device)
            y_fut = _to(batch[FUTURE_DEP_KEY], self.device)
            assert y_past is not None
            assert y_fut is not None

            # train on the batch (user overridable)
            results = self.train_batch(X_past, y_past, X_fut, y_fut)

            if self._train_metrics:
                # move predictions to the host for metric computation
                results.predictions = [p.to('cpu', non_blocking=True) for p in results.predictions]

                utf_targets, utf_preds = self._reverse_tf_batch(batch, results, tf)
                inputs = {k: batch[k].to('cpu').numpy() for k in [PAST_IND_KEY,
                                                                  PAST_DEP_KEY,
                                                                  FUTURE_IND_KEY,
                                                                  FUTURE_DEP_KEY]}
                for metric in self._train_metrics.values():
                    metric.update_state(inputs, utf_targets, utf_preds)

            self._callbacks.on_train_batch_end(epoch, batch_ind, results.loss)

            # augment our loss
            tot_loss += results.loss

        # normalize total loss by number of batches
        mean_loss = tot_loss / (len(dataloader.dataset) / dataloader.batch_size)
        return mean_loss

    def _reverse_tf_batch(self,
                          batch: Mapping[str, torch.Tensor],
                          results: TorchResults,
                          tf: AbstractTransform) -> Tuple[np.ndarray, List[np.ndarray]]:
        """Unbatches a torch.Tensor and undoes any previously applied transforms to reproduce the source data.

        Parameters
        ----------
        batch: Mapping[str, torch.Tensor]
            A batch whose transforms we wish to reverse
        results: TorchResults
            Results from a prediction on the batch
        tf: AbstractTransform
            The transform to undo

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            A tuple of the untransformed targets and untransformed predictions

        """
        if results.predictions is None:
            raise ValueError('`results.predictions` cannot be None')

        # previously: single np.ndarray of shape (batch size, forecast period)
        # now a list (of length batch size) of np.ndarray of shape (1, forecast period)
        # this conversion is necessary as transform.undo operates on a sample, not batch
        transformed_targets = np.concatenate([t[FUTURE_DEP_KEY] for t in unbatch_and_undo(batch, tf)], axis=0)

        # results.predictions is of shape [array(N_batch, N_length), ... X N_pred]
        transformed_preds = []
        for pred in results.predictions:
            transformed_preds.append(
                np.concatenate([p[FUTURE_DEP_KEY] for p in unbatch_and_undo(batch, tf, pred)], axis=0)
            )

        return transformed_targets, transformed_preds

    def train_batch(self,
                    past_regressors: Optional[torch.Tensor], past_targets: torch.Tensor,
                    future_regressors: Optional[torch.Tensor], future_targets: torch.Tensor
                    ) -> TorchResults:
        """Trains the model on a batch of data.

        Parameters
        ----------
        past_regressors: torch.Tensor, optional
            The input covariates which the model should leverage to make predictions
        past_targets: torch.Tensor
            The historical values of the time series which the model should leverage to make predictions
        future_regressors: torch.Tensor, optional
            The future input covariates which the model should leverage to make predictions
        future_targets: torch.Tensor
            The future values of the time series which the model should attempt to predict

        Returns
        -------
        TorchResults
            A summary of the model's results on the batch of data (predictions are located on self.device)

        """
        # forward pass (this should not be called directly by the user, but may be overridden by child classes)
        assert self.optimizer is not None
        self.optimizer.zero_grad()

        # if we have past regressors, cat with targets to form input features
        if past_regressors is not None:
            inputs = torch.cat([past_targets, past_regressors], dim=1)
        else:
            inputs = past_targets

        # if model is future-conditioned, pass future regressors to model
        if self.model.is_future_conditioned:
            predictions = self.model(inputs, future_regressors)
        else:
            predictions = self.model(inputs)

        assert self.loss is not None
        loss = self.loss(predictions, future_targets)

        # backprop
        self._callbacks.on_train_batch_before_backward(loss)
        loss.backward()

        # step
        self._callbacks.on_train_batch_before_step()
        self.optimizer.step()
        return TorchResults(loss=loss.item(),
                            predictions=[p.detach() for p in predictions])

    def _evaluate(self, dataloader: DataLoader, epoch: int) -> float:
        """Evaluate a model on a dataset.

        Parameters
        ----------
        dataloader: torch.utils.data.DataLoader
            The dataloader containing the data which should be evaluated

        Returns
        -------
        float
            The mean per-batch loss for the epoch

        """
        # put the model in eval mode
        prev_model_train = self.model.training
        self.model.eval()

        tot_loss = 0
        tf = dataloader.dataset.transform

        with torch.no_grad():
            for batch_ind, batch in enumerate(dataloader):
                self._callbacks.on_val_batch_begin(epoch, batch_ind)

                # send batch to device
                X_past = _to(batch[PAST_IND_KEY], self.device)
                y_past = _to(batch[PAST_DEP_KEY], self.device)
                X_fut = _to(batch[FUTURE_IND_KEY], self.device)
                y_fut = _to(batch[FUTURE_DEP_KEY], self.device)
                assert y_past is not None
                assert y_fut is not None

                # compute the predictions/loss on self.device
                predictions = self.predict_batch(X_past, y_past, X_fut)

                assert self.loss is not None
                loss = self.loss(predictions, y_fut).item()

                # compute metrics on host
                if self._val_metrics:
                    results = TorchResults(loss=loss,
                                           predictions=[p.to('cpu', non_blocking=True) for p in predictions])

                    utf_targets, utf_preds = self._reverse_tf_batch(batch, results, tf)
                    inputs = {k: batch[k].to('cpu').numpy() for k in [PAST_IND_KEY,
                                                                      PAST_DEP_KEY,
                                                                      FUTURE_IND_KEY,
                                                                      FUTURE_DEP_KEY]}
                    for metric in self._val_metrics.values():
                        metric.update_state(inputs, utf_targets, utf_preds)

                self._callbacks.on_val_batch_end(epoch, batch_ind, loss)

                # augment our loss
                tot_loss += loss

        mean_loss = tot_loss / (len(dataloader.dataset) / dataloader.batch_size)

        # return the model to train mode if necessary
        if prev_model_train:
            self.model.train()

        return mean_loss

    def predict_batch(self,
                      past_regressors: Optional[torch.Tensor], past_targets: torch.Tensor,
                      future_regressors: Optional[torch.Tensor]) -> List[torch.Tensor]:
        """Evaluates a model on a batch of data.

        Parameters
        ----------
        past_regressors: torch.Tensor, optional
            The input covariates which the model should leverage to make predictions
        past_targets: torch.Tensor
            The historical values of the time series which the model should leverage to make predictions
        future_regressors: torch.Tensor, optional
            The future input covariates which the model should leverage to make predictions

        Returns
        -------
        List[torch.Tensor]
            The model's predictions on the batch (predictions are located on self.device)

        """
        # if we have past regressors, cat with targets to form input features
        if past_regressors is not None:
            inputs = torch.cat([past_targets, past_regressors], dim=1)
        else:
            inputs = past_targets

        # if model is future-conditioned, pass future regressors to model
        if self.model.is_future_conditioned:
            predictions = self.model(inputs, future_regressors)
        else:
            predictions = self.model(inputs)

        return [p.detach() for p in predictions]


class RecursiveForecaster(Forecaster):
    """A `RecursiveForecaster` predicts a time series future values by iteratively forecasting one step at a time.

    Note: While teacher forcing is applied during training, during inference the model is fed its own predictions as
    input.
    """

    def __init__(self,
                 model: ForecastingModel,
                 sampler: Callable[[Sequence[torch.Tensor]], torch.Tensor],
                 horizon: int,
                 device: str = 'cuda',
                 metrics: Optional[Union[Metric, Sequence[Metric], Mapping[str, Metric]]] = None,
                 callbacks: Optional[Union[Callback, Sequence[Callback]]] = None):
        """Sequentially forecasts a time series one step at a time.

        Parameters
        ----------
        model: ForecastingModel
            A model with a forecast horizon of 1
        sampler: Callable[[Sequence[torch.Tensor]], torch.Tensor]
            A function mapping the model's output to a single torch.Tensor input for the next time step
        horizon: int
            The number of samples to forecast (completed by repeatedly forecasting a single sample using the model)
        device: str, optional
            The device on which training should occur, defaults to 'cuda'

        """
        super().__init__(model=model,
                         device=device,
                         metrics=metrics,
                         callbacks=callbacks)
        self._horizon = horizon
        self._model_horizon = self.model.head_configs[0].horizon
        self._sampler = sampler

        if self._model_horizon != 1:
            raise ValueError('RecursiveForecaster currently only supports models which forecast 1 period ahead.')

    def train_batch(self,
                    past_regressors: Optional[torch.Tensor], past_targets: torch.Tensor,
                    future_regressors: Optional[torch.Tensor], future_targets: torch.Tensor
                    ) -> TorchResults:
        """Trains the model on a batch of data using teacher forcing.

        Parameters
        ----------
        past_regressors: torch.Tensor, optional
            The input covariates which the model should leverage to make predictions
        past_targets: torch.Tensor
            The historical values of the time series which the model should leverage to make predictions
        future_regressors: torch.Tensor, optional
            The future input covariates which the model should leverage to make predictions
        future_targets: torch.Tensor
            The future values of the time series which the model should attempt to predict

        Returns
        -------
        TorchResults
            A summary of the model's results on the batch of data (predictions are located on self.device)

        """
        assert (past_regressors is not None and future_regressors is not None) or\
               (past_regressors is None and future_regressors is None)

        self.model.retain_state(True)

        # forward pass
        assert self.optimizer is not None
        self.optimizer.zero_grad()

        # warmup with predictions pre-forecast period
        # if we have past regressors, cat with lagged targets to form input features
        if past_regressors is not None:
            inputs = torch.cat([past_targets[:, :, :-1], past_regressors[:, :, 1:]], dim=1)
        else:
            inputs = past_targets[:, :, :-1]
        _ = self.model(inputs)

        # apply teacher forcing
        # cat targets along time axis (use last sample from past targets and all but last from future targets)
        inputs = torch.cat([past_targets[:, :, [-1]], future_targets[:, :, :-1]], dim=2)
        if future_regressors is not None:
            inputs = torch.cat([inputs, future_regressors], dim=1)

        # we predict samples one at a time
        predictions = []
        for i in range(self._horizon):
            preds = self.model(inputs[:, :, [i]])
            predictions.append(preds)

        # predictions: [[p_t1_idx1, p_t1_idx2, ... p_t1_idxN], ... [p_tM_idx1, ... p_tM_idxN]]
        #            : [[p_t1_idx1, p_t2_idx1, ...], ...]
        predictions = [torch.cat(p, dim=2) for p in zip(*predictions)]

        assert self.loss is not None
        loss = self.loss(predictions, future_targets)

        # backprop
        self._callbacks.on_train_batch_before_backward(loss)
        loss.backward()

        # step
        self._callbacks.on_train_batch_before_step()
        self.optimizer.step()

        self.model.retain_state(False)
        return TorchResults(loss=loss.item(),
                            predictions=[p.detach() for p in predictions])

    def predict_batch(self,
                      past_regressors: Optional[torch.Tensor], past_targets: torch.Tensor,
                      future_regressors: Optional[torch.Tensor]) -> List[torch.Tensor]:
        """Evaluates a model on a batch of data by sequentially predicting a single sample at a time.

        Parameters
        ----------
        past_regressors: torch.Tensor, optional
            The input covariates which the model should leverage to make predictions
        past_targets: torch.Tensor
            The historical values of the time series which the model should leverage to make predictions
        future_regressors: torch.Tensor, optional
            The future input covariates which the model should leverage to make predictions

        Returns
        -------
        List[torch.Tensor]
            The model's predictions on the batch (predictions are located on self.device)

        """
        assert (past_regressors is not None and future_regressors is not None) or \
               (past_regressors is None and future_regressors is None)

        self.model.retain_state(True)

        # warmup with predictions pre-forecast period
        # if we have past regressors, cat with lagged targets to form input features
        if past_regressors is not None:
            inputs = torch.cat([past_targets[:, :, :-1], past_regressors[:, :, 1:]], dim=1)
        else:
            inputs = past_targets[:, :, :-1]
        _ = self.model(inputs)

        # we predict samples one head horizon at a time
        predictions = []
        inputs = past_targets[:, :, [-1]]
        for i in range(self._horizon):
            if future_regressors is not None:
                inputs = torch.cat([inputs, future_regressors[:, :, [i]]], dim=1)
            preds = [p.detach() for p in self.model(inputs)]
            predictions.append(preds)
            inputs = self._sampler(preds)

        # predictions: [[p_t1_idx1, p_t1_idx2, ... p_t1_idxN], ... [p_tM_idx1, ... p_tM_idxN]]
        #            : [[p_t1_idx1, p_t2_idx1, ...], ...]
        pred_out = [torch.cat(p, dim=2) for p in zip(*predictions)]

        self.model.retain_state(False)
        return [p.detach() for p in pred_out]
