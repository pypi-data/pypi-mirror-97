from setuptools import setup
from setuptools import find_packages

setup(
    name="log_raider",
    use_scm_version={
        "write_to": "log_raider/version.py",
    },
    packages=find_packages(),
    setup_requires=[
        "setuptools_scm",
    ],
    entry_points={
        "console_scripts": [
            "log_raider_jenkins = log_raider.cli.jenkins:main",
        ],
    },
    author="Joseph Hunkeler",
    author_email="jhunk@stsci.edu",
    url="https://github.com/spactelescope/log_raider",
)
