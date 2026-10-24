"""Checks on the package as a whole, before any algorithm exists."""

import ast
from pathlib import Path

import pytest

import evac

SRC = Path(evac.__file__).parent
DYNAMIC_IMPORTERS = {"import_module", "__import__"}


def networkx_imports(source, filename="<source>"):
    """Line numbers where `source` imports NetworkX, statically or by a literal dynamic import."""
    lines = []
    for node in ast.walk(ast.parse(source, filename=filename)):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        elif isinstance(node, ast.Call):
            func = node.func
            called = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            first = node.args[0] if node.args else None
            literal = isinstance(first, ast.Constant) and isinstance(first.value, str)
            names = [first.value] if called in DYNAMIC_IMPORTERS and literal else []
        else:
            continue
        if any(name.split(".")[0] == "networkx" for name in names):
            lines.append(node.lineno)
    return lines


def test_package_imports():
    assert evac.__version__


def test_src_never_imports_networkx():
    """Hard rule 3: the graded algorithms are our own. NetworkX is a reference for tests only."""
    offenders = [
        f"{path.relative_to(SRC)}:{line}"
        for path in SRC.rglob("*.py")
        for line in networkx_imports(path.read_text(encoding="utf-8"), str(path))
    ]
    assert not offenders, f"networkx imported in src/: {offenders}"


@pytest.mark.parametrize(
    "source",
    [
        "import networkx",
        "import networkx as nx",
        "from networkx.algorithms import flow",
        "import importlib\nimportlib.import_module('networkx')",
        "from importlib import import_module\nimport_module('networkx.algorithms.flow')",
        "__import__('networkx')",
    ],
)
def test_guard_catches_networkx_imports(source):
    assert networkx_imports(source)


@pytest.mark.parametrize(
    "source", ["import heapq", "from collections import deque", "x = 'networkx'"]
)
def test_guard_allows_other_code(source):
    assert not networkx_imports(source)
