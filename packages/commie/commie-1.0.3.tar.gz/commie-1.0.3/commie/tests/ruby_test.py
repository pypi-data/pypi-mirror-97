# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from commie import iter_comments_ruby, Comment


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_ruby(code))


class ShellParserTest(unittest.TestCase):

	def testEmptyString(self):
		code = ""
		comments = commentsToList(code)
		self.assertEqual(len(comments), 0)

	def testComment(self):
		code = '# comment'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '# comment')
		self.assertEqual(comments[0].text, " comment")
		self.assertEqual(comments[0].multiline, False)

	def testCommentInSingleQuotedString(self):
		code = "'this is # not a comment'"
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testCommentInDoubleQuotedString(self):
		code = '"this is # not a comment"'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testNestedStringSingleOutside(self):
		code = "'this is \"# not a comment\"'"
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testNestedStringDoubleOutside(self):
		code = '"this is \'# not a comment\'"'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testEscapedSingleQuote(self):
		code = "\\'# this is a comment"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '# this is a comment')
		self.assertEqual(comments[0].text, " this is a comment")
		self.assertEqual(comments[0].multiline, False)

	def testEscapedDoubleQuote(self):
		code = '\\"# this is a comment'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '# this is a comment')
		self.assertEqual(comments[0].text, " this is a comment")
		self.assertEqual(comments[0].multiline, False)

	def testDoubleComment(self):
		code = '# this is not # another comment'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '# this is not # another comment')
		self.assertEqual(comments[0].text, ' this is not # another comment')
		self.assertEqual(comments[0].multiline, False)

	def testLiteralsSeparatedByComment(self):
		code = r"'This is' # 'a comment'"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "# 'a comment'")
		self.assertEqual(comments[0].text, " 'a comment'")
		self.assertEqual(comments[0].multiline, False)

	def testDifferentLiteralsSeparatedByComment(self):
		code = r''''This is' # "a comment"'''
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '# "a comment"')
		self.assertEqual(comments[0].text, ' "a comment"')
		self.assertEqual(comments[0].multiline, False)
