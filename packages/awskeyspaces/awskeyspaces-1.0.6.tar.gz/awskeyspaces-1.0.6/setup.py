from setuptools import setup
import sys

from pathlib import Path  # noqa E402


CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for  pyproject

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="awskeyspaces",
    use_scm_version={
        "write_to": "src/_pkg_version.py",
        "write_to_template": 'version = "{version}"\n',
    },
    description="AWS KEYSPACES connector Package",
    long_description=long_description,
    long_description_content_type="text/markdown",

    keywords="Cassandra Python3.8 AWS Keyspaces Cassandra",
    author="Julio Quierati",
    author_email="quierati@labunix.dev",
    url="https://bitbucket.com/labunix/keyspaces.git",
    download_url="https://bitbucket.com/labunix/awskeyspaces/get/master.tar.gz",
    packages=['awskeyspaces'],
    package_dir={"": "src"},
    package_data={'': ['*.pem', 'awskeyspaces/*.pem']},
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    install_requires=required,
)
