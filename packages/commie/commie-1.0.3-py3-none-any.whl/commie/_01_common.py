# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import NamedTuple, Optional


class Span(NamedTuple):
	start: int
	end: int

	def extract(self, text: str):
		return text[self.start:self.end]


class Comment:
	"""Represents comments found in a source code string."""

	def __init__(self, source: str, code_span: Span, text_span: Span, multiline: bool):

		self.source = source
		self.code_span: Span = code_span
		self.text_span: Span = text_span
		self.multiline = multiline

		self._text: Optional[str] = None
		self._code: Optional[str] = None

	@property
	def text(self) -> str:
		if self._text is None:
			self._text = self.text_span.extract(self.source)
		return self._text

	@property
	def code(self) -> str:
		if self._code is None:
			self._code = self.code_span.extract(self.source)
		return self._code

	def __repr__(self):
		return f"Comment({repr(self.source)}, {self.code_span}, {self.text_span}, {self.multiline})"

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			if self.__dict__ == other.__dict__:
				return True
		return False


class TestComment(unittest.TestCase):
	def test(self):
		c = Comment("Code /* commented */ like that", Span(5, 20), Span(7, 18), True)
		self.assertEqual(c.code, "/* commented */")
		self.assertEqual(c.text, " commented ")
		self.assertEqual(repr(c),
						 "Comment('Code /* commented */ like that', Span(start=5, end=20), Span(start=7, end=18), True)")
