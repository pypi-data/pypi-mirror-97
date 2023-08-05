# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from commie._01_common import Comment
from .. import iter_comments_html, UnterminatedCommentError


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_html(code))


class HtmlParserTest(unittest.TestCase):

	def testEmptyString(self):
		code = ""
		comments = commentsToList(code)
		self.assertEqual(len(comments), 0)

	def testComment(self):
		code = '<!--comment-->'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "<!--comment-->")
		self.assertEqual(comments[0].text, "comment")
		self.assertEqual(comments[0].multiline, False)

	def testMultilineComment(self):
		code = '<!--multi-line\ncomment-->'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '<!--multi-line\ncomment-->')
		self.assertEqual(comments[0].text, "multi-line\ncomment")
		self.assertEqual(comments[0].multiline, True)

	def testTwoSeparateSingleComment(self):
		code = '<!--comment1-->\n<!--comment2-->'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(comments[0].code, '<!--comment1-->')
		self.assertEqual(comments[0].text, "comment1")
		self.assertEqual(comments[0].multiline, False)

		self.assertEqual(comments[1].code, '<!--comment2-->')
		self.assertEqual(comments[1].text, "comment2")
		self.assertEqual(comments[1].multiline, False)

	def testLayeredComment(self):
		code = '<!-- comment<!-- -->'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '<!-- comment<!-- -->')
		self.assertEqual(comments[0].text, " comment<!-- ")
		self.assertEqual(comments[0].multiline, False)

	def testNonGreedyComment(self):
		code = '<!--i am a comment--> not a comment -->'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '<!--i am a comment-->')
		self.assertEqual(comments[0].text, "i am a comment")
		self.assertEqual(comments[0].multiline, False)

	def testSideBySideComment(self):
		code = '<!--comment1--> ... <!--comment2-->'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(comments[0].code, '<!--comment1-->')
		self.assertEqual(comments[0].text, "comment1")
		self.assertEqual(comments[0].multiline, False)

		self.assertEqual(comments[1].code, '<!--comment2-->')
		self.assertEqual(comments[1].text, "comment2")
		self.assertEqual(comments[1].multiline, False)

	def testUnterminatedComment(self):
		code = '<!--invalid'
		with self.assertRaises(UnterminatedCommentError):
			commentsToList(code)

	def testLonelyTerminator(self):
		code = 'not a comment-->'
		comments = commentsToList(code)
		self.assertEqual(comments, [])
