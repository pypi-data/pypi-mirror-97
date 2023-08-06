from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="conky",
    version="0.0.1.dev1",
    maintainer="David Wharton",
    maintainer_email="whartond@users.noreply.github.com",
    description="Conky",
    long_description=long_description,
    url="https://pypi.org/project/conky",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='<=2.7',
    keywords='conky',
)
