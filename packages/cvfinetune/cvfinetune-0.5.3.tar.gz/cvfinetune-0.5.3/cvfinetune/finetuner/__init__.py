
import logging
try:
	import chainermn
except Exception as e: #pragma: no cover
	_CHAINERMN_AVAILABLE = False #pragma: no cover
else:
	_CHAINERMN_AVAILABLE = True

from cvfinetune import utils
from cvfinetune.finetuner.base import DefaultFinetuner
from cvfinetune.finetuner.mpi import MPIFinetuner

from cvdatasets.utils import pretty_print_dict

class FinetunerFactory(object):

	@classmethod
	def new(cls, opts, default=DefaultFinetuner, mpi_tuner=MPIFinetuner):

		if getattr(opts, "mpi", False):
			assert _CHAINERMN_AVAILABLE, "Distributed training is not possible!"
			msg1 = "MPI enabled. Creating NCCL communicator!"
			comm = chainermn.create_communicator("pure_nccl")
			msg2 = f"Rank: {comm.rank}, IntraRank: {comm.intra_rank}, InterRank: {comm.inter_rank}"

			utils.log_messages([msg1, msg2])
			return cls(mpi_tuner, comm=comm)
		else:
			return cls(default)

	def __init__(self, tuner_cls, **kwargs):
		super(FinetunerFactory, self).__init__()

		self.tuner_cls = tuner_cls
		self.kwargs = kwargs
		logging.info(f"Using {self.tuner_cls.__name__} with arguments: {pretty_print_dict(self.kwargs)}")

	def __call__(self, **kwargs):
		_kwargs = dict(self.kwargs)
		_kwargs.update(kwargs)

		return self.tuner_cls(**_kwargs)

	def get(self, key, default=None):
		return self.kwargs.get(key, default)

	def __getitem__(self, key):
		return self.kwargs[key]

	def __setitem__(self, key, value):
		self.kwargs[key] = value

__all__ = [
	"get_finetuner",
	"DefaultFinetuner",
	"MPIFinetuner",
]
