#!/usr/bin/env python3
#
#  __init__.py
"""
Customised "sphinx_rtd_theme" used by my Python projects.
"""
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import os.path

# 3rd party
import sphinx.writers.html5
import sphinx_rtd_theme  # type: ignore
from docutils import nodes
from docutils.nodes import Element
from sphinx import addnodes
from sphinx.application import Sphinx

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"

__license__: str = "MIT License"
__version__: str = "21.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__version_full__ = __version__

__all__ = ["setup", "HTML5Translator"]


class HTML5Translator(sphinx.writers.html5.HTML5Translator):
	"""
	Custom :class:`sphinx.writers.html5.HTML5Translator` to adjust spacing in bullet pointed lists.
	"""

	def visit_bullet_list(self, node: Element) -> None:  # noqa: D102
		if len(node) == 1 and isinstance(node[0], addnodes.toctree):
			# avoid emitting empty <ul></ul>
			raise nodes.SkipNode

		atts = {}

		old_compact_simple = self.compact_simple  # type: ignore
		self.context.append((self.compact_simple, self.compact_p))  # type: ignore
		self.compact_p = None
		self.compact_simple = self.is_compactable(node)

		classes = []

		if self.compact_simple and not old_compact_simple:
			classes.append("simple")

		if any(len(child) > 1 for child in node):
			classes.append("expanded")

		if classes:
			atts["class"] = ' '.join(classes)

		self.body.append(self.starttag(node, "ul", **atts))

	def visit_enumerated_list(self, node):  # noqa: D102
		atts = {}
		classes = []

		if "start" in node:
			atts["start"] = node["start"]

		if "enumtype" in node:
			classes.append(node["enumtype"])

		if self.is_compactable(node):
			classes.append("simple")

		if any(len(child) > 1 for child in node):
			classes.append("expanded")

		if classes:
			atts["class"] = ' '.join(classes)

		self.body.append(self.starttag(node, "ol", **atts))


def setup(app: Sphinx):
	"""
	Setup Sphinx extension.

	:param app: The Sphinx app.
	"""

	sphinx_rtd_theme.setup(app)

	# add_html_theme is new in Sphinx 1.6+
	if hasattr(app, "add_html_theme"):
		theme_path = os.path.abspath(os.path.dirname(__file__))
		app.add_html_theme("domdf_sphinx_theme", theme_path)

	app.set_translator("html", HTML5Translator, override=True)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}
