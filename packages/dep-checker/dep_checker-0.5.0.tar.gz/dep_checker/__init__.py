#!/usr/bin/env python3
#
#  __init__.py
"""
Tool to check all requirements are actually required.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import ast
import re
import sys
from collections import defaultdict
from typing import Any, Dict, Iterator, List, Optional, Tuple

# 3rd party
import click
from consolekit.terminal_colours import Fore, resolve_color_default
from domdf_python_tools.paths import PathPlus, in_directory
from domdf_python_tools.typing import PathLike
from shippinglabel.requirements import read_requirements
from stdlib_list import stdlib_list  # type: ignore

# this package
from dep_checker.config import AllowedUnused, ConfigReader, NameMapping, NamespacePackages

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.5.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["template", "check_imports"]

if sys.version_info < (3, 10):  # pragma: no cover (py310+)
	libraries = stdlib_list()
else:  # pragma: no cover (<py310)
	libraries = sys.stdlib_module_names

#: The template to use when printing output.
template = "{name} imported on line {lineno} of {filename}"


class Visitor(ast.NodeVisitor):

	def __init__(self, pkg_name: str, namespace_packages: Optional[Dict[str, List[str]]] = None):
		self.import_sources: List[Tuple[str, int]] = []
		self.pkg_name = re.sub("[-.]", '_', pkg_name)
		self.namespace_packages = namespace_packages or {}

	def record_import(self, name: str, lineno: int):
		# TODO: handle ``from namespace import package``

		for namespace in self.namespace_packages:
			if namespace in name:
				name = name.partition(namespace)[1].replace('.', '_')
				break
		else:
			# Not a namespace package
			name = name.split('.')[0]

		if name not in libraries and name != self.pkg_name:
			self.import_sources.append((name, lineno))

	def visit_Import(self, node: ast.Import) -> None:
		name: ast.alias
		for name in node.names:
			self.record_import(name.name, node.lineno)

	def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
		if node.level != 0:
			# relative import
			return

		if node.module:
			self.record_import(node.module, node.lineno)

	def visit(self, node: ast.AST) -> List[Tuple[str, int]]:
		super().visit(node)
		return self.import_sources

	def visit_Try(self, node: ast.Try) -> Any:
		for handler in node.handlers:
			if isinstance(handler.type, ast.Name):
				# print(handler.type.id)

				# TODO: check guarded imports

				if handler.type.id not in {"ImportError", "ModuleNotFoundError"}:
					self.generic_visit(node)

	# def visit_Try(self, node: ast.Try) -> Any:
	# 	for handler in node.handlers:
	# 		if isinstance(handler.type, ast.Attribute):
	# 			# print(handler.type.value.id)
	# 			# print(handler.type.attr)
	# 			pass
	# 		elif isinstance(handler.type, ast.Name):
	# 			# print(handler.type.id)
	# 			if handler.type.id in {"ImportError", "ModuleNotFoundError"}:
	# 				# TODO: check guarded imports
	# 				# print("Guarded")
	# 				pass
	# 			else:
	# 				self.generic_visit(node)
	# 		elif handler.type is None:
	# 			# print(None)
	# 			pass
	# 		else:
	# 			# raise NotImplementedError(type(handler.type))
	# 			pass

	def visit_If(self, node: ast.If) -> Any:
		# TODO: check guarded imports

		if not is_type_checking(node.test):
			self.generic_visit(node)


def is_type_checking(node) -> bool:
	if isinstance(node, ast.NameConstant) and node.value is False:
		return True
	elif isinstance(node, ast.Name) and node.id == "TYPE_CHECKING":
		return True
	elif isinstance(node, ast.Attribute) and node.attr == "TYPE_CHECKING":
		return True
	elif isinstance(node, ast.BoolOp):
		for value in node.values:
			if is_type_checking(value):
				return True

	return False


reader = ConfigReader("dep_checker", default_factory=dict)


def check_imports(
		pkg_name: str,
		req_file: PathLike = "requirements.txt",
		allowed_unused: Optional[List[str]] = None,
		colour: Optional[bool] = None,
		name_mapping: Optional[Dict[str, str]] = None,
		namespace_packages: Optional[List[str]] = None,
		work_dir: PathLike = '.'
		) -> int:
	"""
	Check imports for the given package, against the given requirements file.

	:param pkg_name:
	:param req_file:
	:param allowed_unused: List of requirements which are allowed to be unused in the source code.
	:default allowed_unused: ``[]``
	:param colour: Whether to use coloured output.
	:no-default colour:
	:param name_mapping: Optional mapping of requirement names to import names, if they differ.
	:no-default name_mapping:
	:param namespace_packages: List of namespace packages, e.g. ``ruamel.yaml``.
	:no-default namespace_packages:
	:param work_dir: The directory to find the source of the package in. Useful with the src/ layout.

	| Returns ``0`` if all requirements are used and listed as requirements.
	| Returns ``1`` is a requirement is unused, or if a package is imported but not listed as a requirement.

	.. versionchanged:: 0.5.0 Added the ``name_mapping`` option.

	.. versionchanged:: 0.5.0 Added the ``work_dir`` option.
	"""

	ret = 0
	config = reader.visit()
	colour = resolve_color_default(colour)

	if allowed_unused is None:
		allowed_unused = AllowedUnused.get(config)

	if name_mapping is None:
		name_mapping = NameMapping.get(config)

	if namespace_packages is None:
		namespace_packages = NamespacePackages.get(config)

	work_dir = PathPlus(work_dir)
	req_file = PathPlus(req_file)

	if not req_file.is_absolute():
		req_file = work_dir / req_file

	req_names: List[str] = []

	for req in read_requirements(req_file)[0]:
		name = req.name.replace('-', '_')
		if name in name_mapping:
			# replace names in req_names with the name of the package the requirement provides
			req_names.append(name_mapping[name])
		else:
			req_names.append(name)

	req_names.sort()

	imports: Dict[str, Dict[PathPlus, int]] = defaultdict(dict)
	# mapping of import name to mapping of filename to lineno where imported

	with in_directory(work_dir):

		for filename in iter_files_to_check(work_dir, pkg_name):

			visitor = Visitor(pkg_name.replace('/', '.'), namespace_packages)  # type: ignore
			file_content = filename.read_text()

			for import_name, lineno in visitor.visit(ast.parse(file_content)):

				if import_name not in req_names:
					# Not listed as requirement

					if re.match(r".*#\s*nodep.*", file_content.splitlines()[lineno - 1]):
						# Marked with "# nodep", so the user wants to ignore this
						continue

					msg = template.format(name=import_name, lineno=lineno, filename=filename.as_posix())
					click.echo(Fore.RED(f"✘ {msg} but not listed as a requirement"), color=colour)
					ret |= 1

				else:
					min_lineno = min((imports[import_name].get(filename, lineno), lineno))
					imports[import_name][filename] = min_lineno

	for req_name in req_names:
		for filename, lineno in imports[req_name].items():
			# Imported and listed as requirement
			msg = template.format(name=req_name, lineno=lineno, filename=filename.as_posix())
			click.echo(Fore.GREEN(f"✔ {msg}"), color=colour)
			break
		else:
			if req_name not in allowed_unused:
				# not imported
				click.echo(Fore.YELLOW(f"✘ {req_name} never imported"), color=colour)
				ret |= 1

	return ret


def iter_files_to_check(basepath: PathLike, pkg_name: str) -> Iterator[PathPlus]:
	"""
	Returns an iterator over all files in ``pkg_name``.

	If ``pkg_name`` resolves to a single-file module, that is the only element of the iterator.

	.. versionadded:: $VERSION

	:param basepath:
	:param pkg_name:

	:raises FileNotFoundError: If neither :file:`{<pkg_name>}.py` or the directory ``pkg_name`` is found.
	"""

	basepath = PathPlus(basepath)

	if (basepath / f"{pkg_name}.py").is_file():
		yield PathPlus(f"{pkg_name}.py")
		return

	if not (basepath / pkg_name).exists():
		raise FileNotFoundError(f"Can't find a package called {pkg_name!r} in {basepath.as_posix()}.")

	for filename in (basepath / pkg_name.replace('.', '/')).rglob("*.py"):
		filename = filename.relative_to(basepath)

		if filename.parts[0] in {".tox", "venv", ".venv"}:  # pragma: no cover
			continue

		yield filename
