# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

from typing import Iterable

from commie._01_common import Comment, Span


def extract_comments(code: str) -> Iterable[Comment]:
	"""Extracts a list of comments from the given shell script.
	Comments are represented with the Comment class found in the common module.
	Shell script comments only come in one form, single-line. Single line
	comments start with an unquoted or unescaped '#' and continue on until the
	end of the line. A quoted '#' is one that is located within a pair of
	matching single or double quote marks. An escaped '#' is one that is
	immediately preceeded by a backslash '\'
	Args:
	  code: String containing code to extract comments from.
	Returns:
	  Python list of common.Comment in the order that they appear in the code.
	"""

	DEFAULT = 0
	IN_COMMENT = 1
	IN_STRING = 2
	ESCAPING_CHAR_INSIDE_STRING = 3
	ESCAPING_CHAR_OUTSIDE_OF_STRING = 4

	state = DEFAULT
	string_char = ''
	current_comment_text = ''
	line_counter = 1

	comment_start_pos = None
	position = -1

	for position, char in enumerate(code):
		if state == DEFAULT:
			# Waiting for comment start character, beginning of string,
			# or escape character.
			if char == '#':
				state = IN_COMMENT
				comment_start_pos = position
			elif char in ('"', "'"):
				string_char = char
				state = IN_STRING
			elif char == '\\':
				state = ESCAPING_CHAR_OUTSIDE_OF_STRING
		elif state == IN_COMMENT:
			if char == '\n':
				yield Comment(code, code_span=Span(comment_start_pos, position),
							  text_span=Span(comment_start_pos + 1, position), multiline=False)
				current_comment_text = ''
				state = DEFAULT
			else:
				current_comment_text += char
		elif state == IN_STRING:
			if char == string_char:
				state = DEFAULT
			elif char == '\\':
				state = ESCAPING_CHAR_INSIDE_STRING
		elif state == ESCAPING_CHAR_INSIDE_STRING:
			state = IN_STRING
		elif state == ESCAPING_CHAR_OUTSIDE_OF_STRING:
			# Escaping current char, outside of string.
			state = DEFAULT
		if char == '\n':
			line_counter += 1

	# end of file

	if state == IN_COMMENT:
		yield Comment(code, code_span=Span(comment_start_pos, position + 1),
					  text_span=Span(comment_start_pos + 1, position + 1), multiline=False)
