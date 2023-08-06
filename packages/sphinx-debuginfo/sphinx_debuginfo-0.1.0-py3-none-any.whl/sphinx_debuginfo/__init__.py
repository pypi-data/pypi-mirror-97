#!/usr/bin/env python3
#
#  __init__.py
"""
A Sphinx extension to include debugging information in the output.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Any, Dict

# 3rd party
import tabulate
from domdf_python_tools.compat import importlib_metadata
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["setup", "write_debug_info"]


def write_debug_info(app: Sphinx, exception: Exception = None) -> None:
	"""
	Write the file(s) containing debugging information.

	:param app:
	:param exception:
	"""

	if exception:  # pragma: no cover
		return

	if app.builder.format.lower() != "html":
		return

	packages = []

	distribution: importlib_metadata.PathDistribution
	for distribution in importlib_metadata.distributions():
		packages.append((distribution.name, distribution.version))

	packages.sort(key=lambda x: x[0].lower())

	debug_dir = PathPlus(app.outdir) / "_debug"
	debug_dir.maybe_make()

	table = tabulate.tabulate(packages, headers=("Name", "Version"), tablefmt="html", colalign=("left", "right"))

	(debug_dir / "index.html").write_lines([
			"<h3>Packages and versions used to build these docs:<h3>",
			'',
			table,
			])


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`sphinx-debuginfo`.

	:param app: The Sphinx app.
	"""

	app.connect("build-finished", write_debug_info)

	return {"parallel_read_safe": True, "version": __version__}
