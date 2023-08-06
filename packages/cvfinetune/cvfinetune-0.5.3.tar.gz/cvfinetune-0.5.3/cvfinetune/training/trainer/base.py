import logging
from os.path import join, basename
from datetime import datetime

import chainer
from chainer.training import extensions, Trainer as T
from chainer.training import trigger as trigger_module
from chainer_addons.training import lr_shift
from chainer_addons.training.optimizer import OptimizerType
from chainer_addons.training.extensions.learning_rate import CosineAnnealingLearningRate
from chainer_addons.training.extensions import AlternateTrainable, SwitchTrainables, WarmUp

from cvdatasets.utils import attr_dict

default_intervals = attr_dict(
	print =		(1,  'epoch'),
	log =		(1,  'epoch'),
	eval =		(1,  'epoch'),
	snapshot =	(10, 'epoch'),
)

def debug_hook(trainer):
	pass
	# print(trainer.updater.get_optimizer("main").target.model.fc6.W.data.mean(), file=open("debug.out", "a"))


def _is_adam(opts):
	return opts.optimizer == OptimizerType.ADAM.name.lower()

class Trainer(T):
	_default_base_model = "model"

	def __init__(self, opts, updater, evaluator=None, weights=None, intervals=default_intervals, no_observe=False):

		self._only_eval = opts.only_eval
		if weights is None or weights == "auto":
			self.base_model = self._default_base_model
		else:
			self.base_model, _, _ = basename(weights).rpartition(".")

		optimizer = updater.get_optimizer("main")
		# adam has some specific attributes, so we need to check this
		is_adam = _is_adam(opts)
		clf = optimizer.target
		model = clf.model

		if no_observe:
			outdir = opts.output
		else:
			outdir = self.output_directory(opts)
			logging.info("Training outputs are saved under \"{}\"".format(outdir))

		super(Trainer, self).__init__(
			updater=updater,
			stop_trigger=(opts.epochs, 'epoch'),
			out=outdir
		)

		### Evaluator ###
		self.evaluator = evaluator
		if evaluator is not None:
			self.extend(evaluator, trigger=intervals.eval)

		### Warm up ###
		lr_offset = 0
		if opts.warm_up:
			assert opts.warm_up > 0, "Warm-up argument must be positive!"
			lr_offset = opts.warm_up

			warm_up_lr = opts.learning_rate
			logging.info("Warm-up of {} epochs enabled!".format(opts.warm_up))
			self.extend(WarmUp(
				opts.warm_up, model,
				opts.learning_rate, warm_up_lr))


		### LR shift ###
		if opts.cosine_schedule is not None and opts.cosine_schedule > 0:
			lr_shift_ext = CosineAnnealingLearningRate(
				attr="alpha" if is_adam else "lr",
				lr=opts.learning_rate,
				target=opts.lr_target,
				epochs=opts.epochs,
				offset=lr_offset,
				stages=opts.cosine_schedule
			)
			new_epochs = lr_shift_ext._epochs
			self.stop_trigger = trigger_module.get_trigger((new_epochs, "epoch"))
			self.extend(lr_shift_ext)
		else:
			lr_shift_ext = lr_shift(optimizer,
				init=opts.learning_rate,
				rate=opts.lr_decrease_rate, target=opts.lr_target)
			self.extend(lr_shift_ext, trigger=(opts.lr_shift, 'epoch'))

		### Code below is only for "main" Trainers ###
		if no_observe: return

		self.extend(extensions.observe_lr(), trigger=intervals.log)
		self.extend(extensions.LogReport(trigger=intervals.log))

		### Snapshotting ###
		self.setup_snapshots(opts, clf.model, intervals.snapshot)

		### Reports and Plots ###
		print_values, plot_values = self.reportables(opts)
		self.extend(extensions.PrintReport(print_values), trigger=intervals.print)
		for name, values in plot_values.items():
			ext = extensions.PlotReport(values, 'epoch', file_name='{}.png'.format(name))
			self.extend(ext)

		### Progress bar ###
		if not opts.no_progress:
			self.extend(extensions.ProgressBar(update_interval=1))

	def setup_snapshots(self, opts, obj, trigger):

		if opts.no_snapshot:
			logging.warning("Models are not snapshot!")
		else:
			dump_fmt = "ft_model_epoch{0.updater.epoch:03d}.npz"
			self.extend(extensions.snapshot_object(obj, dump_fmt), trigger=trigger)
			logging.info("Snapshot format: \"{}\"".format(dump_fmt))

	def eval_name(self, name):
		if self.evaluator is None:
			return name

		return f"{self.evaluator.default_name}/{name}"

	def reportables(self, opts):

		print_values = [
			"elapsed_time",
			"epoch",
			# "lr",

			"main/accuracy", self.eval_name("main/accuracy"),
			"main/loss", self.eval_name("main/loss"),

		]

		plot_values = {
			"accuracy": [
				"main/accuracy",  self.eval_name("main/accuracy"),
			],
			"loss": [
				"main/loss", self.eval_name("main/loss"),
			],
		}

		return print_values, plot_values


	def output_directory(self, opts):

		result = opts.output

		if self.base_model != self._default_base_model:
			result = join(result, self.base_model)

		result = join(result, datetime.now().strftime("%Y-%m-%d-%H.%M.%S.%f"))
		return result

	def run(self, init_eval=True):
		if init_eval:
			logging.info("Evaluating initial model ...")
			init_perf = self.evaluator(self)
			values = {key: float(value) for key, value in init_perf.items()}

			msg = []

			if "val/main/accuracy" in values:
				msg.append("Initial accuracy: {val/main/accuracy:.3%}".format(**values))

			if "val/main/loss" in values:
				msg.append("Initial loss: {val/main/loss:.3f}".format(**values))

			logging.info(" ".join(msg))

		if self._only_eval:
			return
		return super(Trainer, self).run()

