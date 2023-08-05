# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from pathlib import Path
from typing import Iterable, Union

from commie._01_common import Comment
from commie._01_errors import *
from commie.parsers import *


def pickfunc(filename: str):
	filename = filename.lower()
	ext = filename.rpartition(".")[-1]

	if ext in ["c", "cpp", "java",
			   "h", "hpp",
			   # Objective-C source code 'implementation' program files usually
			   # have .m filename extensions, while Objective-C 'header/interface' files
			   # have .h extensions
			   "m"]:
		return iter_comments_c

	if ext in ["go"]:
		return iter_comments_go

	if ext in ["js", "ts", "dart"]:
		return iter_comments_c

	if ext in ["html", "htm", "xml"]:
		return iter_comments_html

	if ext in ["rb"]:
		return iter_comments_ruby

	if ext in ["py"]:
		return iter_comments_python

	if ext in ["scss"]:
		return iter_comments_sass

	if ext in ["css"]:
		return iter_comments_css

	if ext in ["sh"]:
		return iter_comments_shell

	raise FormatUndetectedError


class TestPickFunc(unittest.TestCase):
	def test_html(self):
		self.assertEqual(pickfunc(filename="file.html"), iter_comments_html)
		self.assertEqual(pickfunc(filename="1991.HTM"), iter_comments_html)

	def test_js(self):
		self.assertEqual(pickfunc(filename="file.dart"), iter_comments_c)
		self.assertEqual(pickfunc(filename="file.js"), iter_comments_c)

	def test_undetected(self):
		with self.assertRaises(FormatUndetectedError):
			pickfunc(filename="ladeda.haha")


def iter_comments_str(code: str, filename: str) -> Iterable[Comment]:
	func = pickfunc(filename)
	return func(code)


def iter_comments_file(file: Path) -> Iterable[Comment]:
	return iter_comments_str(file.read_text(), file.name)


def iter_comments(codeOrFile: Union[Path, str], filename: str = None) -> Iterable[Comment]:
	if isinstance(codeOrFile, str):
		if filename is None:
			raise ValueError("Please specify filename")
		return iter_comments_str(codeOrFile, filename)
	return iter_comments_file(codeOrFile)


class TestIterComments(unittest.TestCase):
	def testNoFilename(self):
		with self.assertRaises(ValueError):
			list(iter_comments("..."))
