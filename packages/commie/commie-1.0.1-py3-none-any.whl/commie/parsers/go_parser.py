# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

from typing import Iterable

from commie.parsers import common
from commie.parsers.common import Comment, Span


def extract_comments(goCode: str) -> Iterable[Comment]:
	"""Extracts a list of comments from the given Go source code.

	Comments are represented with the Comment class found in the common module.
	Go comments come in two forms, single and multi-line comments.
	  - Single-line comments begin with '//' and continue to the end of line.
	  - Multi-line comments begin with '/*' and end with '*/' and can span
		multiple lines of code. If a multi-line comment does not terminate
		before EOF is reached, then an exception is raised.
	Go comments are not allowed to start in a string or rune literal. This
	module makes sure to watch out for those.

	https://golang.org/ref/spec#Comments

	Args:
	  goCode: String containing code to extract comments from.
	Returns:
	  Python list of common.Comment in the order that they appear in the code.
	Raises:
	  common.UnterminatedCommentError: Encountered an unterminated multi-line
		comment.
	"""

	DEFAULT = 0
	AFTER_SLASH = 1
	IN_SINGLE_LINE_COMMENT = 2
	IN_MULTI_LINE_COMMENT = 3
	IN_MULTI_LINE_COMMENT_ASTERISK = 4
	IN_STRING = 5
	IN_STRING_ESCAPING = 6

	state = DEFAULT
	current_comment = ''

	line_counter = 1
	string_char = ''

	position = -1
	comment_start_pos = None

	for position, char in enumerate(goCode):
		if state == DEFAULT:
			# Waiting for comment start character or beginning of
			# string or rune literal.
			if char == '/':
				state = AFTER_SLASH
			elif char in ('"', "'", '`'):
				string_char = char
				state = IN_STRING
		elif state == AFTER_SLASH:
			# Found comment start character, classify next character and
			# determine if single or multi-line comment.
			if char == '/':
				state = IN_SINGLE_LINE_COMMENT
				comment_start_pos = position - 1
			elif char == '*':
				comment_start = line_counter
				state = IN_MULTI_LINE_COMMENT
				comment_start_pos = position - 1
			else:
				state = DEFAULT
		elif state == IN_SINGLE_LINE_COMMENT:
			# In single-line comment, read characters util EOL.
			if char == '\n':
				yield Comment(goCode, Span(comment_start_pos, position + 1),
							  Span(comment_start_pos + 2, position + 1), False)
				# yield Comment(current_comment, comment_start_pos, position+1, False)
				current_comment = ''
				state = 0
			else:
				current_comment += char
		elif state == IN_MULTI_LINE_COMMENT:
			# In multi-line comment, add characters until '*' is
			# encountered.
			if char == '*':
				state = IN_MULTI_LINE_COMMENT_ASTERISK
			else:
				current_comment += char
		elif state == IN_MULTI_LINE_COMMENT_ASTERISK:
			# In multi-line comment with asterisk found. Determine if
			# comment is ending.
			if char == '/':
				yield Comment(goCode, Span(comment_start_pos, position + 1),
							  Span(comment_start_pos + 2, position - 1), True)
				current_comment = ''
				state = DEFAULT
			else:
				current_comment += '*'
				# Care for multiple '*' in a row
				if char != '*':
					current_comment += char
					state = IN_MULTI_LINE_COMMENT
		elif state == IN_STRING:
			# In string literal, expect literal end or escape character.
			if char == string_char:
				state = DEFAULT
			elif char == '\\':
				state = IN_STRING_ESCAPING
		elif state == IN_STRING_ESCAPING:
			# In string literal, escaping current char.
			state = IN_STRING
		if char == '\n':
			line_counter += 1

	# EOF

	if state in (IN_MULTI_LINE_COMMENT, IN_MULTI_LINE_COMMENT_ASTERISK):
		raise common.UnterminatedCommentError()
	if state == IN_SINGLE_LINE_COMMENT:
		# was in single-line comment
		yield Comment(goCode, Span(comment_start_pos, position + 1),
					  Span(comment_start_pos + 2, position + 1), False)

	# yield Comment(current_comment, comment_start_pos, position+1, False)
