# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

# AG 2021: in pypi/comment_parser this module was only for parsing JavaScript.
# But in fact, it coped better with parsing C than old regex-based c_parser.py.
# So for now it is the default parsed for all C-like languages.
#
# The most evident difference between JS and C in that single quotes can
# contain a string in JS, but in C and C++ they are only for single chars.
# However, for the task, individual characters within single quotes are
# hardly different from single-letter strings.
#
# The parser for Go now also relies on the following code. In fact, the only
# key differnce in Go parsed was `backquoted strings` support

from enum import IntEnum, auto
from typing import Iterable

import commie._01_errors
from commie import _01_common
from commie._01_common import Comment, Span


def iter_comments_c(source: str) -> Iterable[Comment]:
	return _iter_comments_universal(source, "\"'")


def iter_comments_go(source: str) -> Iterable[Comment]:
	return _iter_comments_universal(source, "\"'`")


def _iter_comments_universal(source: str, string_quote_chars: str) -> Iterable[Comment]:
	class State(IntEnum):

		DEFAULT = auto()
		IN_SINGLE_LINE_COMMENT = auto()
		IN_MULTI_LINE_COMMENT = auto()
		IN_MULTI_LINE_COMMENT_AFTER_ASTERISK = auto()
		IN_STRING = auto()
		IN_STRING_AFTER_BACKSLASH = auto()
		FOUND_SLASH = auto()

	state: State = State.DEFAULT

	comment_start_pos = None

	quote = None
	position = 0

	for position, char in enumerate(source):

		if state == State.DEFAULT:
			# waiting for comment start character or beginning of a string
			if char == '/':
				state = State.FOUND_SLASH
			elif char in string_quote_chars:
				quote = char
				state = State.IN_STRING
		elif state == State.FOUND_SLASH:
			# found comment start character, classify next character and
			# determine if single or multi-line comment.
			if char == '/':
				state = State.IN_SINGLE_LINE_COMMENT
				comment_start_pos = position - 1  # we are at second char of "//"
			elif char == '*':
				state = State.IN_MULTI_LINE_COMMENT
				comment_start_pos = position - 1  # we are at second char of "/*"
			else:
				state = State.DEFAULT
		elif state == State.IN_SINGLE_LINE_COMMENT:
			# in single-line comment, reading characters until EOL
			if char == '\n':
				yield _01_common.Comment(
					source,
					text_span=Span(comment_start_pos + 2, position),
					code_span=Span(comment_start_pos, position),
					multiline=False)
				state = State.DEFAULT
		elif state == State.IN_MULTI_LINE_COMMENT:
			# in multi-line comment, add characters until '*' is encountered
			if char == '*':
				state = State.IN_MULTI_LINE_COMMENT_AFTER_ASTERISK
		elif state == State.IN_MULTI_LINE_COMMENT_AFTER_ASTERISK:
			# In multi-line comment with asterisk found. Determine if
			# comment is ending.
			if char == '/':
				yield Comment(
					source,
					text_span=Span(comment_start_pos + 2, position - 1),
					code_span=Span(comment_start_pos, position + 1),
					multiline=True)
				state = State.DEFAULT
			else:
				# care for multiple '*' in a row
				if char != '*':
					state = State.IN_MULTI_LINE_COMMENT
		elif state == State.IN_STRING:
			# in string literal, expect literal end or escape character.
			if char == quote:
				state = State.DEFAULT
			elif char == '\\':
				state = State.IN_STRING_AFTER_BACKSLASH
		elif state == State.IN_STRING_AFTER_BACKSLASH:
			state = State.IN_STRING

	# end of file
	if state in (State.IN_MULTI_LINE_COMMENT, State.IN_MULTI_LINE_COMMENT_AFTER_ASTERISK):
		raise commie._01_errors.UnterminatedCommentError()

	if state == State.IN_SINGLE_LINE_COMMENT:
		yield _01_common.Comment(
			source,
			text_span=Span(comment_start_pos + 2, position + 1),
			code_span=Span(comment_start_pos, position + 1),
			multiline=False)
