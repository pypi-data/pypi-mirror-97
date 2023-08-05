# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

# AG 2021: This was named js_parser.py in comment_parser@pypi.
# But not it is used for parsing C code as well.

from typing import Iterable, Optional

from commie.parsers import common
from commie.parsers.common import Comment, Span


def extract_comments(source: str) -> Iterable[Comment]:
	"""Extracts a list of comments from C-like source code.

	C-like comments come in two forms, single and multi-line comments.
	  - Single-line comments begin with '//' and continue to the end of line.
	  - Multi-line comments begin with '/*' and end with '*/' and can span
		multiple lines of code. If a multi-line comment does not terminate
		before EOF is reached, then an exception is raised.

	This module takes quoted strings into account when extracting comments from
	source code.
	"""

	WAITING_FOR_COMMENT = 0
	IN_SINGLE_LINE_COMMENT = 2
	IN_MULTI_LINE_COMMENT = 3
	IN_MULTI_LINE_COMMENT_ASTERISK = 4
	IN_STRING = 5
	IN_STRING_ESCAPE_NEXT_CHAR = 6
	FOUND_SLASH = 1

	state:int = WAITING_FOR_COMMENT

	markup_start_pos = None
	text_start_pos: Optional[int] = 0
	text_length: Optional[int] = 0

	quote = None
	position = 0

	for position, char in enumerate(source):

		if state == WAITING_FOR_COMMENT:
			# Waiting for comment start character or beginning of
			# string.
			if char == '/':
				state = FOUND_SLASH
			elif char in ('"', "'"):
				quote = char
				state = IN_STRING
		elif state == FOUND_SLASH:
			# Found comment start character, classify next character and
			# determine if single or multi-line comment.
			if char == '/':
				state = IN_SINGLE_LINE_COMMENT
				markup_start_pos = position - 1  # we are at second char of "//"
				text_start_pos = position + 1
			elif char == '*':
				state = IN_MULTI_LINE_COMMENT
				markup_start_pos = position - 1  # we are at second char of "/*"
				text_start_pos = position + 1
			else:
				state = WAITING_FOR_COMMENT
		elif state == IN_SINGLE_LINE_COMMENT:
			# In single-line comment, read characters until EOL.
			if char == '\n':
				yield common.Comment(
					source,
					text_span=Span(text_start_pos, text_start_pos + text_length),
					code_span=Span(markup_start_pos, position),
					multiline=False)
				text_length = 0
				state = WAITING_FOR_COMMENT
			else:
				text_length += 1
		elif state == IN_MULTI_LINE_COMMENT:
			# In multi-line comment, add characters until '*' is
			# encountered.
			if char == '*':
				state = IN_MULTI_LINE_COMMENT_ASTERISK
			else:
				text_length += 1
		elif state == IN_MULTI_LINE_COMMENT_ASTERISK:
			# In multi-line comment with asterisk found. Determine if
			# comment is ending.
			if char == '/':
				yield Comment(
					source,
					text_span=Span(text_start_pos, text_start_pos + text_length),
					code_span=Span(markup_start_pos, position + 1),
					multiline=True)
				text_length = 0
				state = WAITING_FOR_COMMENT
			else:
				text_length += 1
				# Care for multiple '*' in a row
				if char != '*':
					text_length += 1
					state = IN_MULTI_LINE_COMMENT
		elif state == IN_STRING:
			# In string literal, expect literal end or escape character.
			if char == quote:
				state = WAITING_FOR_COMMENT
			elif char == '\\':
				state = IN_STRING_ESCAPE_NEXT_CHAR
		elif state == IN_STRING_ESCAPE_NEXT_CHAR:
			state = IN_STRING
		if char == '\n':
			pass

	# end of file
	if state in (IN_MULTI_LINE_COMMENT, IN_MULTI_LINE_COMMENT_ASTERISK):
		raise common.UnterminatedCommentError()

	if state == IN_SINGLE_LINE_COMMENT:
		yield common.Comment(
			source,
			text_span=Span(text_start_pos, text_start_pos + text_length),
			code_span=Span(markup_start_pos, position + 1),
			multiline=False)
