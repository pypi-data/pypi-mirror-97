# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from commie import iter_comments_c
from commie.parsers.common import Comment, UnterminatedCommentError
from commie.tests.helper import minimize


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_c(code))
	#return list(iter_comments_c(code))


class CParserTest(unittest.TestCase):

	def testSimpleMain(self):
		code = "// this is a comment\nint main() {\nreturn 0;\n}\n"
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, "// this is a comment")
		self.assertEqual(comments[0].text, " this is a comment")
		self.assertEqual(comments[0].multiline, False)

	def testSingleLineComment(self):
		code = '// single line comment'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '// single line comment')
		self.assertEqual(comments[0].text, " single line comment")
		self.assertEqual(comments[0].multiline, False)

	def testSingleLineCommentInStringLiteral(self):
		code = 'char* msg = "// this is not a comment"'
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

		self.assertEqual(comments[0].code, '/***************/')
		self.assertEqual(comments[0].text, "*************")
		self.assertEqual(comments[0].multiline, True)

	def testMultiLineCommentInStringLiteral(self):
		code = 'char* msg = "/* This is not a\\nmultiline comment */"'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testMultiLineCommentUnterminated(self):
		code = 'int a = 1; /* Unterminated\\n comment'
		with self.assertRaises(UnterminatedCommentError):
			commentsToList(code)

	def testMultipleMultilineComments(self):
		code = '/* abc */ /* 123 */'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(comments[0].code, '/* abc */')
		self.assertEqual(comments[0].text, " abc ")
		self.assertEqual(comments[0].multiline, True)

		self.assertEqual(comments[1].code, '/* 123 */')
		self.assertEqual(comments[1].text, " 123 ")
		self.assertEqual(comments[1].multiline, True)

	def testStringThenComment(self):
		code = r'"" /* "abc */'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '/* "abc */')
		self.assertEqual(comments[0].text, ' "abc ')
		self.assertEqual(comments[0].multiline, True)

	def testCommentStartInsideEscapedQuotesInStringLiteral(self):
		#FIXME: This one fails with UnterminatedCommentError
		code = r'" \" /* \" "'
		comments = commentsToList(code)
		self.assertEqual(comments, [])
		pass

	def testStringEscapedBackslashCharacter(self):
		code = r'"\\"'
		comments = commentsToList(code)
		self.assertEqual(comments, [])

	def testTwoStringsFollowedByComment(self):
		code = r'"""" // foo'
		comments = commentsToList(code)

		self.assertEqual(len(comments), 1)

		self.assertEqual(comments[0].code, '// foo')
		self.assertEqual(comments[0].text, " foo")
		self.assertEqual(comments[0].multiline, False)

	def testCommentedMultilineComment(self):
		code = '''// What if i start a /* here
    		int main(){return 0;}
    		// and ended it here */'''

		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(comments[0].code, '// What if i start a /* here')
		self.assertEqual(comments[0].text, " What if i start a /* here")
		self.assertEqual(comments[0].multiline, False)

		self.assertEqual(comments[1].code, '// and ended it here */')
		self.assertEqual(comments[1].text, " and ended it here */")
		self.assertEqual(comments[1].multiline, False)

	def testMultilineCommentedComment(self):
		code = '''
			/*// here
			int main(){return 0;}
			*/// and ended it here */
		'''

		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(minimize(comments[0].code), "/*// here int main(){return 0;} */")
		self.assertEqual(minimize(comments[0].text), "// here int main(){return 0;}")
		self.assertEqual(comments[0].multiline, True)

		self.assertEqual(comments[1].code, '// and ended it here */')
		self.assertEqual(comments[1].text, " and ended it here */")
		self.assertEqual(comments[1].multiline, False)

	def testFragment(self):
		code = """
		
		/**
		 * JSDoc is rarely used to annotate C.
		 *
		 * @param: abc
		 */		
	
		int main() { return 42; } 
	
		// comment at eof"""

		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(minimize(comments[0].code),
						 '/** * JSDoc is rarely used to annotate C. * * @param: abc */')
		self.assertEqual(minimize(comments[0].text),
						 '* * JSDoc is rarely used to annotate C. * * @param: abc')
		self.assertEqual(comments[0].multiline, True)

		self.assertEqual(comments[1].code, '// comment at eof')
		self.assertEqual(comments[1].text, ' comment at eof')
		self.assertEqual(comments[1].multiline, False)

