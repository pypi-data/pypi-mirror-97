# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

import re
from typing import Iterable

from commie.parsers import common
from commie.parsers.common import Comment
from commie.parsers.helper import matchGroupToComment


def extract_comments(cssCode: str) -> Iterable[Comment]:
	pattern = r"""
    (?P<comment> /\*(?P<content>(.|\n)*?)?\*/) |
    (?P<error> /\*(.*)?)
  """

	for match in re.finditer(pattern, cssCode, flags=re.VERBOSE | re.MULTILINE):

		kind = match.lastgroup

		if kind == "comment":
			yield matchGroupToComment(match, "content", True)

		elif kind == "error":
			raise common.UnterminatedCommentError()
