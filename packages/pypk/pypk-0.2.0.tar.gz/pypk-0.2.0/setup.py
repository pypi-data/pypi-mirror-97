from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).parent
README = HERE.joinpath("README.md").read_text()

setup(
    name="pypk",
    author="Miller Wilt",
    author_email="miller@pyriteai.com",
    description="An opinionated Python package template generator",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PyriteAI/pypk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    use_scm_version={"write_to": "src/pypk/version.py"},
    setup_requires=["setuptools_scm"],
    python_requires=">=3.6.0",
)
