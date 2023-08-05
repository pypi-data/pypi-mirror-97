# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-License-Identifier: BSD-3-Clause

import re

from commie._01_common import Comment, Span


def matchGroupToComment(match: re.Match, groupName: str, multiline: bool) -> Comment:
	fullSpan = match.span()

	fullText = match.group(0)
	innerText = match.group(groupName)
	textStart = fullText.index(innerText)
	assert textStart >= 0

	return Comment(
		match.string,
		text_span=Span(fullSpan[0] + textStart, fullSpan[0] + textStart + len(innerText)),
		code_span=Span(fullSpan[0], fullSpan[1]),
		multiline=multiline)
