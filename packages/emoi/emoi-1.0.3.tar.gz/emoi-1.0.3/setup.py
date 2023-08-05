from setuptools import find_packages, setup

from emoi import __version__

from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="emoi",
    version=__version__,
    description="emoi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://trobz.com",
    author="Trobz",
    author_email="contact@trobz.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["click>=7", "trobz"],
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Software Development",
    ],
    zip_safe=False,
    entry_points="""
        [console_scripts]
        emoi=emoi.cli:main
    """,
)
