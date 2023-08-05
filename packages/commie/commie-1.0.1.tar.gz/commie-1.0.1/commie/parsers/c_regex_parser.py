# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

# AG 2021: This parser was used as the default for C in comment_parser@pypi.
# But the JS parser is much better at this task. Even in the comment_parser@pypi,
# there was a test that failed  with this parser, but worked fine with JS.
#
# The parser will remain here for now, but will be used for C.


import re
from typing import Iterable

from commie.parsers import common
from commie.parsers.common import Comment
from commie.parsers.helper import matchGroupToComment


def extract_comments(code: str) -> Iterable[Comment]:
	"""Extracts a list of comments from the given C family source code.

	Comments are represented with the Comment class found in the common module.
	C family comments come in two forms, single and multi-line comments.
	  - Single-line comments begin with '//' and continue to the end of line.
	  - Multi-line comments begin with '/*' and end with '*/' and can span
		multiple lines of code. If a multi-line comment does not terminate
		before EOF is reached, then an exception is raised.

	!!! Note that this doesn't take language-specific preprocessor directives into
	consideration.

	"""
	pattern = r"""
		(?P<literal> (\"([^\"\n])*\")+) |
		(?P<single> //(?P<single_content>.*)?$) |
		(?P<multi> /\*(?P<multi_content>(.|\n)*?)?\*/) |
		(?P<error> /\*(.*)?)
	  """

	compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)

	for match in compiled.finditer(code):

		kind = match.lastgroup
		# markupSpan = match.span(0)

		if kind == "single":
			yield matchGroupToComment(match, "single_content", False)

		elif kind == "multi":
			yield matchGroupToComment(match, "multi_content", True)

		elif kind == "error":
			raise common.UnterminatedCommentError()
