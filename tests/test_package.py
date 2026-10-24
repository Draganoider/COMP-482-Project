"""Checks on the package as a whole, before any algorithm exists."""

import ast
from pathlib import Path

import evac

SRC = Path(evac.__file__).parent


def test_package_imports():
    assert evac.__version__


def test_src_never_imports_networkx():
    """Hard rule 3: the graded algorithms are our own. NetworkX is a reference for tests only."""
    offenders = []
    for path in SRC.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            else:
                continue
            if any(name.split(".")[0] == "networkx" for name in names):
                offenders.append(f"{path.relative_to(SRC)}:{node.lineno}")
    assert not offenders, f"networkx imported in src/: {offenders}"
