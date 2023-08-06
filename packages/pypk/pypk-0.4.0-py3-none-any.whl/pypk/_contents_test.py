from . import _contents


def test_pyproject():
    expected = """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 120
target-version = ["py36"]

[tool.isort]
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 120
"""
    actual = _contents.PYPROJECT.format(package_name="foo", target_version="py36")
    assert actual == expected


def test_readme():
    expected = """# foo
"""
    actual = _contents.README.format(package_name="foo")
    assert actual == expected


def test_setup():
    expected = """from setuptools import find_packages, setup

setup(
    name="foo",
    author="bar",
    author_email="baz@cool.com",
    description="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.6.0",
)
"""
    actual = _contents.SETUP.format(
        package_name="foo", author="bar", author_email="baz@cool.com", python_version="3.6.0"
    )
    assert actual == expected


def test_precommit():
    expected = """# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-json
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/PyCQA/isort
    rev: 5.7.0
    hooks:
      - id: isort
  - repo: https://github.com/psf/black
    rev: 20.8b1
    hooks:
      - id: black
        language_version: python3
  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.4
    hooks:
      - id: flake8
        additional_dependencies: [flake8-bugbear]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.0
    hooks:
      - id: bandit
        args: ["-x", "*/**/*_test.py"]
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest src/foo
        language: system
        pass_filenames: false
        types: [python]
"""
    actual = _contents.PRECOMMIT.format(package_name="foo")
    assert actual == expected
