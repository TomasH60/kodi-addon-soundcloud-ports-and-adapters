#!/usr/bin/env python3
import argparse
import ast
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "venv",
    ".venv",
    "env",
    ".env",
    "node_modules",
    "dist",
    "build",
}


@dataclass(frozen=True)
class Counts:
    total: int
    within_package: int
    outside_package: int
    xbmc_related: int


def iter_py_files(root: Path, exclude_dirs: set[str]) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs and not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".py") and not fn.startswith("."):
                yield Path(dirpath) / fn


def is_internal_module(module: str, root: Path) -> bool:
    if not module:
        return False
    parts = module.split(".")
    py_file = root.joinpath(*parts).with_suffix(".py")
    pkg_init = root.joinpath(*parts, "__init__.py")
    return py_file.exists() or pkg_init.exists()


def has_xbmc_token(s: str) -> bool:
    return "xbmc" in (s or "").lower()


def count_imports_in_file(path: Path, root: Path) -> Counts:
    try:
        src = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        src = path.read_text(encoding="latin-1")

    try:
        tree = ast.parse(src, filename=str(path))
    except SyntaxError:
        return Counts(total=0, within_package=0, outside_package=0, xbmc_related=0)

    total = 0
    within_pkg = 0
    outside = 0
    xbmc_related = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                total += 1
                if is_internal_module(alias.name, root):
                    within_pkg += 1
                else:
                    outside += 1
                if has_xbmc_token(alias.name):
                    xbmc_related += 1

        elif isinstance(node, ast.ImportFrom):
            total += 1

            is_pkg = False
            if getattr(node, "level", 0) and node.level > 0:
                is_pkg = True
            else:
                mod = node.module or ""
                is_pkg = is_internal_module(mod, root)

            if is_pkg:
                within_pkg += 1
            else:
                outside += 1

            mod = node.module or ""
            if has_xbmc_token(mod):
                xbmc_related += 1
            else:
                for alias in node.names:
                    if has_xbmc_token(alias.name):
                        xbmc_related += 1
                        break

    return Counts(total=total, within_package=within_pkg, outside_package=outside, xbmc_related=xbmc_related)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "root",
        nargs="?",
        default=None,
        help="Root directory to scan (defaults to current working directory).",
    )
    p.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Directory name to exclude (can be repeated).",
    )
    args = p.parse_args()

    root = Path(args.root).resolve() if args.root else Path.cwd().resolve()
    if root.is_file():
        root = root.parent

    exclude = set(DEFAULT_EXCLUDE_DIRS)
    exclude.update(args.exclude_dir)

    total = 0
    within_pkg = 0
    outside = 0
    xbmc_related = 0

    for py_file in iter_py_files(root, exclude):
        c = count_imports_in_file(py_file, root)
        total += c.total
        within_pkg += c.within_package
        outside += c.outside_package
        xbmc_related += c.xbmc_related

    print(f"total={total}")
    print(f"package={within_pkg}")
    print(f"other={outside}")
    print(f"xbmc_related={xbmc_related}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
