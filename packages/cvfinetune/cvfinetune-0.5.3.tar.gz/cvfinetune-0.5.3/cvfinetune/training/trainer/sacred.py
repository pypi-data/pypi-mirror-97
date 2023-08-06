from cvfinetune.training.trainer.base import Trainer, default_intervals
from chainer_addons.training.sacred import SacredTrainerMixin

class SacredTrainer(SacredTrainerMixin, Trainer):

	def __init__(self, intervals=default_intervals, *args, **kwargs):
		super(SacredTrainer, self).__init__(
			intervals=intervals, sacred_trigger=intervals.log, *args, **kwargs)
