import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="azunyan",
    version="2.0.2",
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

## upgrade
# python3 -m pip install --user --upgrade setuptools wheel twine
## pack
# python3 setup.py sdist bdist_wheel
## upload
# python3 -m twine upload dist/*
## clean
# rm azunyan.egg-info build dist
## upgrade
# python3 -m pip install --upgrade azunyan -i https://pypi.org/simple/
