import distutils.cmd
import os
import re
import sys

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)

SEMVER_REGEX = r"(?P<semver>(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)"  # noqa: E501
VERSION_RE = re.compile(r'__version__ = "' + SEMVER_REGEX + r'"')


def get_version():
    init = open(os.path.join(ROOT, "mondobrain", "__init__.py")).read()
    return VERSION_RE.search(init).group("semver")


class VerifyVersionCommand(distutils.cmd.Command):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    user_options = [
        ("git-tag=", None, "Tag to verify"),
        ("git-branch=", None, "Branch to verify"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.git_tag = os.getenv("CIRCLE_TAG")
        self.git_branch = os.getenv("CIRCLE_BRANCH")

    def finalize_options(self):
        pass

    def run(self):
        git_version = self.git_tag

        if git_version is None:
            branch = self.git_branch or "NO TAG/RELEASE BRANCH"
            _, _, git_version = branch.partition("release/")

        print(git_version)
        version = get_version()

        if git_version != version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                git_version, version
            )
            sys.exit(info)


setup(
    name="mondobrain",
    version=get_version(),
    description="MondoBrain API wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MondoBrain",
    url="https://bitbucket.org/mondobrain/mondobrain-python",
    project_urls={
        "MondoBrain homepage": "https://mondobrain.com",
        "MondoBrain source": "https://bitbucket.org/mondobrain/mondobrain-python",
    },
    packages=find_packages(exclude=["tests*"], include=["mondobrain", "mondobrain.*"]),
    package_data={"mondobrain": ["examples/*.md", "datasets/data/*.csv"]},
    include_package_data=True,
    license="MIT License",
    classifiers=[
        # How mature is this project?
        "Development Status :: 3 - Alpha",
        # Intended audience
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        # Language of project
        "Natural Language :: English",
        # License
        "License :: OSI Approved :: MIT License",
        # Versions supported
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # Operating systems
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    platforms="any",
    python_requires=">=3.6",
    install_requires=[
        "auth0-python ~= 3.13.0",
        "numpy ~= 1.18.1",
        "pandas ~= 1.0.1",
        "pyarrow ~= 0.16.0",
        "requests ~= 2.7",
        "scikit-learn ~= 0.22.1",
    ],
    # extras_require={
    # "nlp": ["solver @ git+https://bitbucket.org/mondobrain/indigo@70569bb"]
    # },
    extras_require={
        "viz": ["graphviz ~= 0.14.2", "networkx ~= 2.5", "pygraphviz ~= 1.6"]
    },
    cmdclass={"verify": VerifyVersionCommand},
)
