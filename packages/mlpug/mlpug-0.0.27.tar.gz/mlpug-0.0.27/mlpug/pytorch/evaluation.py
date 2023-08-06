import os

import abc

import torch
import torch.distributed as dist

from mlpug.trainers.training import BatchChunkingResults
from mlpug.evaluation import default_metric_reducer_func, MetricEvaluatorBase

from mlpug.utils import is_chunkable

from basics.base import Base
from basics.logging import get_logger

logger = get_logger(os.path.basename(__file__))


# ####### DEFAULT GATHER LOSS METHODS ########
class GatherLossBase(Base, metaclass=abc.ABCMeta):

    def __init__(self, name, delete_training_loss=True, delete_auxiliary_results=True, requester=None):
        if requester is not None:
            name += f'[{requester}]'

        super(GatherLossBase, self).__init__(pybase_logger_name=name)

        self._delete_training_loss = delete_training_loss
        self._delete_auxiliary_results = delete_auxiliary_results

        self.requester = requester

        self._gather_loss_func = None
        if dist.is_initialized():
            self._log.info(f"Using distributed gather masked loss function")
            self._gather_loss_func = self._gather_loss_distributed
        else:
            self._log.info(f"Using gather masked loss function")
            self._gather_loss_func = self._gather_loss

    def _do_detatch_auxiliary_results(self, auxiliary_results):
        # When auxiliary_results is a BatchChunkingResults list, it was created by batch chunking
        if type(auxiliary_results) is BatchChunkingResults:
            for aux in auxiliary_results:
                aux[0].detach_()
                aux[1].detach_()
        else:
            auxiliary_results[0].detach_()
            auxiliary_results[1].detach_()

    def _do_delete_auxiliary_results(self, auxiliary_results):
        # When auxiliary_results is a BatchChunkingResults list, it was created by batch chunking
        if type(auxiliary_results) is BatchChunkingResults:
            for (ls, ns) in auxiliary_results:
                del ls
                del ns
        else:
            (ls, ns) = auxiliary_results
            del ls
            del ns

    @abc.abstractmethod
    def __call__(self, loss, auxiliary_results, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def _gather_loss(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def _gather_loss_distributed(self, **kwargs):
        raise NotImplementedError()


class GatherLossSimple(GatherLossBase):

    def __init__(self, delete_training_loss=True, requester=None):
        super().__init__("GatherLossSimple", delete_training_loss, requester)

    def __call__(self, loss, **kwargs):
        training_loss = loss
        training_loss.detach_()

        loss, loss_sum, num_samples = self._gather_loss_func(loss=training_loss, **kwargs)

        if self._delete_training_loss:
            del training_loss

        return loss, loss_sum, num_samples

    def _gather_loss(self, loss, **kwargs):
        loss = loss.item()
        return loss, loss, 1

    def _gather_loss_distributed(self, loss, **kwargs):
        loss_sum = loss
        dist.reduce(loss_sum, 0)
        num_devices = dist.get_world_size()
        loss = loss_sum / num_devices

        return loss.item(), loss_sum.item(), num_devices


class GatherMaskedLoss(GatherLossBase):

    def __init__(self, delete_training_loss=True, delete_auxiliary_results=True, requester=None):
        super().__init__("GatherMaskedLoss", delete_training_loss, delete_auxiliary_results, requester)

    def __call__(self, loss, auxiliary_results, **kwargs):
        training_loss = loss
        training_loss.detach_()

        self._do_detatch_auxiliary_results(auxiliary_results)

        # When auxiliary_results is a BatchChunkingResults list, it was created by batch chunking
        if type(auxiliary_results) is BatchChunkingResults:
            loss_sum = 0
            num_samples = 0
            for aux in auxiliary_results:
                loss_sum += aux[0]
                num_samples += aux[1]
        else:
            loss_sum = auxiliary_results[0]
            num_samples = auxiliary_results[1]

        loss, loss_sum, num_samples = self._gather_loss_func(loss_sum=loss_sum, num_samples=num_samples, **kwargs)

        if self._delete_training_loss:
            del training_loss

        if self._delete_auxiliary_results:
            self._do_delete_auxiliary_results(auxiliary_results)

        return loss, loss_sum, num_samples

    def _gather_loss(self, loss_sum, num_samples, **kwargs):
        loss_sum = loss_sum.item()
        num_samples = num_samples.item()

        loss = loss_sum/num_samples

        return loss, loss_sum, num_samples

    def _gather_loss_distributed(self, loss_sum, num_samples, **kwargs):
        dist.reduce(loss_sum, 0)
        dist.reduce(num_samples, 0)

        loss_sum = loss_sum.item()
        num_samples = num_samples.item()

        loss = loss_sum / num_samples

        return loss, loss_sum, num_samples
# ############################################


class MetricEvaluator(MetricEvaluatorBase):

    def __init__(self, *args, batch_metric_funcs=None, name="MetricEvaluator", **kwargs):

        if batch_metric_funcs is None:
            batch_metric_funcs = {
                "loss": GatherLossSimple(requester=name)
            }

        super().__init__(batch_metric_funcs, *args, name=name, **kwargs)

    def _create_default_model_evaluate_func(self):

        def evaluate_loss(batch, evaluate_settings=None):
            if is_chunkable(batch):
                # Get raw batch
                batch = batch[:]

            with torch.no_grad():
                results = self._trainer.evaluate_loss(
                    batch,
                    inference_mode=True,
                    evaluate_settings=evaluate_settings)

            return results

        return evaluate_loss

