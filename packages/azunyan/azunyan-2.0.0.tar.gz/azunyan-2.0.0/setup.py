import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="azunyan",
    version="2.0.0",
    author="Elypha",
    author_email="i@elypha.com",
    description="Some simple functions I packed for self usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Elypha/azunyan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
