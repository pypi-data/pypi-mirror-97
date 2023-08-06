import os
import warnings

from cvargparse import BaseParser
from cvdatasets.utils import read_info_file
from functools import wraps


WARNING = """Could not find default info file \"{}\". """ + \
"""Some arguments (dataset, parts etc.) are not restraint to certain choices! """ + \
"""You can set <DATA> environment variable to change the default info file location."""

DEFAULT_INFO_FILE = os.environ.get("DATA")
def get_info_file():

	if DEFAULT_INFO_FILE is not None and os.path.isfile(DEFAULT_INFO_FILE):
		return read_info_file(DEFAULT_INFO_FILE)
	else:
		warnings.warn(WARNING.format(DEFAULT_INFO_FILE))
		return None


def parser_extender(extender):

	@wraps(extender)
	def inner(parser):
		assert isinstance(parser, BaseParser), \
			"Parser should be an BaseParser instance!"

		extender(parser)

		return parser

	return inner
