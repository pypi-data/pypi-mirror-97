# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import re
from typing import Iterable

from commie.parsers.common import Comment
from commie.parsers.helper import matchGroupToComment


def extract_comments(rubyCode: str) -> Iterable[Comment]:
	"""Extracts a list of comments from the given Ruby source code.

	Comments are represented with the Comment class found in the common module.

	Ruby comments start with a '#' character and run to the end of the line,
	http://ruby-doc.com/docs/ProgrammingRuby.

	Args:
	  rubyCode: String containing code to extract comments from.
	Returns:
	  Python list of common.Comment in the order that they appear in the code..
	"""
	pattern = r"""
		(?P<literal> ([\"'])((?:\\\2|(?:(?!\2)).)*)(\2)) |
		(?P<single> \#(?P<single_content>.*?)$)
	  """
	compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)

	comments = []
	for match in compiled.finditer(rubyCode):
		kind = match.lastgroup

		if kind == "single":
			yield matchGroupToComment(match, "single_content", False)

	return comments
