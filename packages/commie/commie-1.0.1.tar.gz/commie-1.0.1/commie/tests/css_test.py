# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from commie import iter_comments_css
from ..parsers.common import Comment


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_css(code))


class CssParserTest(unittest.TestCase):

	def testSimpleMain(self):
		code = ".cssClass { /* i am\n a comment! */ }"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "/* i am\n a comment! */")
		self.assertEqual(comments[0].text, " i am\n a comment! ")
		self.assertEqual(comments[0].multiline, True)

	def testIncLeft(self):
		code = ".cssClass { /* /* i am a comment! */ }"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "/* /* i am a comment! */")
		self.assertEqual(comments[0].text, " /* i am a comment! ")
		self.assertEqual(comments[0].multiline, True)

	def testIncRight(self):
		code = ".cssClass { /* i am a comment! */ */ }"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "/* i am a comment! */")
		self.assertEqual(comments[0].text, " i am a comment! ")
		self.assertEqual(comments[0].multiline, True)

	def testThreeComments(self):
		code = """
    
    /* THIS IS A CSS CODE
       WITH MULTILINE COMMENTS */
    
    body {margin: 0; /* comment inside */}
    p {margin: 1px; ) /* comment outside */
    
    """
		comments = commentsToList(code)

		self.assertEqual(len(comments), 3)
