from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="infinstor",
    version="1.1.7",
    author="InfinStor, Inc.",
    author_email="support@infinstor.com",
    license="AGPL-3.0",
    description="InfinStor Utilities usually run in ipython from jupyterlab cells",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://infinstor.com/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=["notebook", "boto3", "pandas", "tqdm", "astor", "infinstor-mlflow-plugin"],
    python_requires='>=3.6',
)
