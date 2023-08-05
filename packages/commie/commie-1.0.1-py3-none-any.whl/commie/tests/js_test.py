# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from .helper import minimize
from .. import iter_comments_c
from ..parsers.common import Comment, UnterminatedCommentError


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_c(code))


class CParserJsTest(unittest.TestCase):

	def testSingleLineComment(self):
		code = '// single line comment'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "// single line comment")
		self.assertEqual(comments[0].text, " single line comment")
		self.assertEqual(comments[0].multiline, False)

	def testLineCommentInSingleQuotedLiteral(self):
		code = "msg = '// this is not a comment'"
		comments = commentsToList(code)
		self.assertEqual(len(comments), 0)

	def testLineCommentInDoubleQuotedLiteral(self):
		code = 'msg = "// this is not a comment"'
		comments = commentsToList(code)
		self.assertEqual(len(comments), 0)

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
		self.assertEqual(comments[0].code, '/***************/')
		self.assertEqual(comments[0].text, "*************")
		self.assertEqual(comments[0].multiline, True)

	def testMultiLineCommentInSingleLiteral(self):
		code = "msg = '/* This is not a\\nmultiline comment */'"
		comments = commentsToList(code)
		self.assertEqual(len(comments), 0)

	def testMultiLineCommentInDoubleLiteral(self):
		code = 'msg = "/* This is not a\\nmultiline comment */"'
		comments = commentsToList(code)
		self.assertEqual(len(comments), 0)

	def testMultiLineCommentUnterminated(self):
		code = 'a = 1 /* Unterminated\\n comment'
		with self.assertRaises(UnterminatedCommentError):
			commentsToList(code)

	def testFragment(self):
		code = """
		
		/**
		 * JSDoc is used to annotate JavaScript.
		 *
		 * @author: Wikipedia
		 */
		 
		// single line comment
	
		let forgetIt = prompt("What?");
		
		// comment at eof"""

		comments = commentsToList(code)

		self.assertEqual(len(comments), 3)

		self.assertEqual(minimize(comments[0].code),
						 '/** * JSDoc is used to annotate JavaScript. * * @author: Wikipedia */')
		self.assertEqual(minimize(comments[0].text),
						 '* * JSDoc is used to annotate JavaScript. * * @author: Wikipedia')
		self.assertEqual(comments[0].multiline, True)

		self.assertEqual(comments[1].code, '// single line comment')
		self.assertEqual(comments[1].text, ' single line comment')
		self.assertEqual(comments[1].multiline, False)


		self.assertEqual(comments[2].code, '// comment at eof')
		self.assertEqual(comments[2].text, ' comment at eof')
		self.assertEqual(comments[2].multiline, False)
