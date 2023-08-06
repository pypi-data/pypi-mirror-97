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
