from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="testwizard.testobjects-core",
    version="3.3.0",
    author="Eurofins Digital Testing - Belgium",
    author_email="support-be@eurofins.com",
    description="Testwizard core components for testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    install_requires=[
        'testwizard.commands-services==3.3.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)






