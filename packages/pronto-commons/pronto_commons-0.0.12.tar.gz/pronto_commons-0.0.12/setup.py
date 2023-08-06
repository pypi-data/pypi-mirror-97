import os
import pathlib
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install

VERSION = "0.0.12"

HERE = pathlib.Path(__file__).parent
TESTS_REQUIRE = []

# Except is created so it doesn't break when installing, since this file is not shipped when deploying on PyPi
try:
    TESTS_REQUIRE = (HERE / "test-requirements.txt").read_text().splitlines()
except:
    pass


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="pronto_commons",
    packages=find_packages(exclude=["tests", "tests*", "*requirements*"]),
    version=VERSION,
    description="Pronto common methods and entities used on the products backend",
    author="Pronto development <dev@tupronto.mx>",
    author_email="dev@tupronto.mx",
    license="MIT",
    url="https://bitbucket.org/tuprontomx/pronto_commons",
    keywords=["Pronto", "Commons"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="pronto_commons.tests",
    setup_requires=["flake8", "pytest-runner"],
    tests_require=TESTS_REQUIRE,
    python_requires=">=3",
    cmdclass={
        "verify": VerifyVersionCommand,
    },
)
