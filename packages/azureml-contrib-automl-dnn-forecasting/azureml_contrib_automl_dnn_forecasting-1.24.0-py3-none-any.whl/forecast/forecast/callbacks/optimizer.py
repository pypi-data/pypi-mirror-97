"""Callbacks which integrate with and/or modify the behavior of model optimizers."""

from typing import Mapping, Optional
from typing_extensions import Literal

from torch.optim.lr_scheduler import _LRScheduler, ReduceLROnPlateau

from forecast.callbacks import Callback
from forecast.utils import EarlyTerminationException


class LRScheduleCallback(Callback):
    """Wraps a generic learning rate schedule in a callback."""

    def __init__(self, sched: _LRScheduler):
        """Wraps a generic learning rate schedule in a callback.

        Parameters
        ----------
        sched: _LRScheduler
            A learning rate scheduler which only requires the current epoch to step

        """
        super().__init__()
        self._sched = sched

    def on_train_val_epoch_end(self, epoch: int) -> None:
        """Steps the learning rate scheduler.

        Parameters
        ----------
        epoch: int
            The current epoch

        Returns
        -------
        None

        """
        self._sched.step(epoch)


class ReduceLROnPlateauCallback(Callback):
    """Wraps a ReduceLROnPlateau schedule in a callback."""

    def __init__(self, sched: ReduceLROnPlateau, metric_name: str):
        """Wraps a ReduceLROnPlateau schedule in a callback.

        Parameters
        ----------
        sched: ReduceLROnPlateau
            The learning rate schedule
        metric_name: str
            The name of the metric to be examined for plateau (or 'loss' if the loss function should be monitored)

        """
        super().__init__()
        self._sched = sched
        self._metric_name = metric_name

    def on_val_end(self, epoch: int, loss: float, metrics: Mapping[str, float]) -> None:
        """Examines whether the specified metric has plateaued.

        Parameters
        ----------
        epoch: int
            The current epoch
        loss: float
            The current value of the loss
        metrics: Mapping[str, float]
            The model's performance on the validation set during the current epoch

        Returns
        -------
        None

        """
        if self._metric_name == 'loss':
            m = loss
        else:
            m = metrics[self._metric_name]
        self._sched.step(m, epoch)


class EarlyStoppingCallback(Callback):
    def __init__(
            self,
            patience: int,
            min_improvement: float,
            metric: Optional[str] = None,
            mode: Literal["min", "max"] = 'min',
            improvement_type: Literal["relative", "absolute"] = 'relative'
    ):
        """Prematurely ends the training regimen in the val loss doesn't improve for a fixed number of epochs.

        Parameters
        ----------
        patience: int
            The number of epochs to wait for improvement before forcing termiantion
        min_improvement: float
            The size of the improvement required to be marked as a "realized" improvement
        metric: Optional[str]
            If None, uses the val loss to assess improvement. Otherwise, uses the specified metric. Defaults to None.
        mode: Literal["min", "max"]
            Whether the target value should decrease or increase in value. Defaults to min.
        improvement_type: Literal["relative", "absolute"]
            Whether the min_improvement specifies an absolute improvement value or a percent improvement. Defaults to
            relative.
        """
        super().__init__()

        if patience < 0:
            raise ValueError("Parameter `patience` must be >= 0.")
        if min_improvement <= 0:
            raise ValueError("Parameter `min_improvement` must be > 0.")

        self.patience = patience
        self.steps_since_improvement = 0
        self.best_score = float('inf')
        self.metric = metric
        self._terminate = False

        mode = mode.lower()
        if mode not in ('min', 'max'):
            raise ValueError('Parameter `mode` must be one of ("min", "max").')
        self.mode = mode
        if self.mode == "min":
            min_improvement *= -1

        improvement_type = improvement_type.lower()
        if improvement_type not in ('relative', 'absolute'):
            raise ValueError('Parameter `improvement_type` must be one of ("relative", "absolute").')
        self.improvement_type = improvement_type
        if self.improvement_type == "relative":
            min_improvement += 1

        self.min_improvement = min_improvement

    def _get_thresh(self) -> float:
        if self.mode == "relative":
            return self.best_score * self.min_improvement
        else:
            return self.best_score + self.min_improvement

    def on_val_end(self, epoch: int, loss: float, metrics: Mapping[str, float]) -> None:
        score = loss if self.metric is None else metrics[self.metric]
        thresh = self._get_thresh()
        improved = score <= thresh if self.mode == "min" else score >= thresh

        if improved:
            self.steps_since_improvement = 0
            self.best_score = score
        else:
            self.steps_since_improvement += 1

        if self.steps_since_improvement >= self.patience:
            self._terminate = True

    def on_train_val_epoch_end(self, epoch: int) -> None:
        if self._terminate:
            raise EarlyTerminationException
