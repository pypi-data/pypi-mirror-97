
from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="delphai-ml-utils",
    version="0.1.0",
    description="A Python package to manage kube secrets.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/delphai/delphai-ml-utils",
    author="ahmed",
    author_email="ahmed.mahmoud@delphai.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ml_utils"],
    include_package_data=True,
    install_requires=[
        'python-dotenv', 'coloredlogs',
        'kubernetes', 'keyring', 'azure-storage-blob', 'confuse'],
)