"""Checks on the package as a whole, before any algorithm exists."""

import ast
from pathlib import Path

import pytest

import evac

SRC = Path(evac.__file__).parent
DYNAMIC_IMPORTERS = {"import_module", "__import__"}


def networkx_imports(source, filename="<source>"):
    """Line numbers where `source` imports NetworkX, statically or by a literal dynamic import.

    Dynamic imports are caught when the module name is a string literal, passed by position or as
    `name=`, including through an alias (`from importlib import import_module as load`).
    """
    tree = ast.parse(source, filename=filename)
    importers = set(DYNAMIC_IMPORTERS)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "importlib":
            importers |= {a.asname for a in node.names if a.name == "import_module" and a.asname}
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        elif isinstance(node, ast.Call):
            func = node.func
            called = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            args = node.args[:1] + [k.value for k in node.keywords if k.arg == "name"]
            literals = [a.value for a in args if isinstance(a, ast.Constant)]
            names = [v for v in literals if isinstance(v, str)] if called in importers else []
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
        "import importlib\nimportlib.import_module(name='networkx')",
        "from importlib import import_module as load\nload('networkx')",
    ],
)
def test_guard_catches_networkx_imports(source):
    assert networkx_imports(source)


@pytest.mark.parametrize(
    "source", ["import heapq", "from collections import deque", "x = 'networkx'"]
)
def test_guard_allows_other_code(source):
    assert not networkx_imports(source)
