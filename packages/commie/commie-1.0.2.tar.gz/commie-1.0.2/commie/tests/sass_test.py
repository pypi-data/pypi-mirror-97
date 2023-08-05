# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

import unittest
from typing import List

from commie import iter_comments_sass
from ..parsers.common import Comment


def commentsToList(code: str) -> List[Comment]:
	return list(iter_comments_sass(code))


class SassParserTest(unittest.TestCase):

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
    		/* Welcome to Compass.
			 * In this file you should write your main styles. (or centralize your imports)
			 * Import this file using the following HTML or equivalent:
			 * <link href="/stylesheets/screen.css" media="screen, projection" rel="stylesheet" type="text/css" /> */
			
			@import "compass/reset";
			
			@import "compass/reset";
			@import "compass/css3";
			@import "compass/layout";
			@import "compass/utilities";
			@import "compass/utilities/general/clearfix";
			@import "compass/css3/pie";
			@import "compass/css3/transform";
			
			
			//Uses Sass' color modifying functions to adjust colors
			
			$color1: #a9c4e5;
			$color2: darken($color1, 40);
			$fontcolor1: darken($color1, 80);
			$fontcolor2: lighten($color1, 50);
			$border-radius: 4px;
			
			
			@import "basics";
    
    	"""
		comments = commentsToList(code)

		self.assertEqual(len(comments), 2)

		self.assertEqual(len(comments[0].code.splitlines()), 4)
		self.assertEqual(len(comments[1].code.splitlines()), 1)
