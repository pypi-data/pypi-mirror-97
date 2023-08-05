# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import io
import tokenize
from typing import NamedTuple, Iterable

from commie._01_common import Comment, Span


class PosToken(NamedTuple):
	tokenType: int
	text: str
	start: int
	end: int


def postokenize(infile: io.BytesIO) -> Iterable[PosToken]:
	# based on https://stackoverflow.com/a/62761208 (CC BY-SA 4.0)

	# Used to track starting position of each line.
	# Note that tokenize starts line numbers at 1 and column numbers at 0
	offsets = [0]

	def wrapped_readline():
		# Function used to wrap calls to infile.readline(); stores current
		# stream position at the beginning of each line.
		offsets.append(infile.tell())
		return infile.readline()

	# For each returned token, substitute type with exact_type and
	# add token boundaries as stream positions
	for t in tokenize.tokenize(wrapped_readline):
		startline, startcol = t.start
		endline, endcol = t.end
		yield PosToken(t.exact_type, t.string,
					   offsets[startline] + startcol,
					   offsets[endline] + endcol)


def extract_comments(code: str) -> Iterable[Comment]:
	"""Extracts a list of comments from the given Python script.
	Comments are identified using the tokenize module. Does not include function,
	class, or module docstrings. All comments are single line comments.
	Args:
	  code: String containing code to extract comments from.
	Returns:
	  Python list of common.Comment in the order that they appear in the code.
	Raises:
	  tokenize.TokenError
	"""

	for token in postokenize(io.BytesIO(code.encode())):
		if token.tokenType == tokenize.COMMENT:
			yield Comment(
				code,
				text_span=Span(token.start + 1, token.end),
				code_span=Span(token.start, token.end),
				multiline=False
			)


if __name__ == "__main__":
	def experiment():
		from pathlib import Path
		extract_comments(Path(__file__).read_text())


	experiment()
