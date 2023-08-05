# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from .. import iter_comments_go, Comment, UnterminatedCommentError


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_go(code))


class GoParserTest(unittest.TestCase):

	def testSingleLineComment(self):
		code = '// single line comment'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "// single line comment")
		self.assertEqual(comments[0].text, " single line comment")
		self.assertEqual(comments[0].multiline, False)

	def testSingleLineCommentInRuneLiteral(self):
		code = "msg := '// this is not a comment'"
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testSingleLineCommentInBackTickedLiteral(self):
		code = "msg := `// this is not a comment`"
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testSingleLineCommentInQuotedLiteral(self):
		code = 'msg := "// this is not a comment"'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testMultiLineComment(self):
		code = '/* multiline\ncomment */'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '/* multiline\ncomment */')
		self.assertEqual(comments[0].text, " multiline\ncomment ")
		self.assertEqual(comments[0].multiline, True)

	def testMultiLineCommentWithStars(self):
		code = "/***************/"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "/***************/")
		self.assertEqual(comments[0].text, "*************")
		self.assertEqual(comments[0].multiline, True)

	def testMultiLineCommentInRuneLiteral(self):
		code = "msg := '/* This is not a\\nmultiline comment */'"
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testMultiLineCommentInQuotedLiteral(self):
		code = 'msg := "/* This is not a\\nmultiline comment */"'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testMultiLineCommentInBackTickedLiteral(self):
		code = 'msg := `/* This is not a\\nmultiline comment */`'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testMultiLineCommentUnterminated(self):
		code = 'a := 1 /* Unterminated\\n comment'
		with self.assertRaises(UnterminatedCommentError):
			commentsToList(code)
