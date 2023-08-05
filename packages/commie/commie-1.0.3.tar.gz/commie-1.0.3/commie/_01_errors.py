# SPDX-FileCopyrightText: Copyright (c) 2021 Art Galkin <ortemeo@gmail.com>
# SPDX-FileCopyrightText: Copyright (c) 2015 Jean-Ralph Aviles
# SPDX-License-Identifier: BSD-3-Clause

class Error(Exception):
	"""Base Error class for all comment parsers."""


class FileError(Error):
	"""Raised if there is an issue reading a file."""


class UnterminatedCommentError(Error):
	"""Raised if an Unterminated multi-line comment is encountered."""


class FormatUndetectedError(Error):
	"""Raised if there is an issue reading a file."""
