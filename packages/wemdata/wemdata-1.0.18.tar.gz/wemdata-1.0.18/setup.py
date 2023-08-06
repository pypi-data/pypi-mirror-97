import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wemdata", # Replace with your own username
    version="1.0.18",
    author="Ignatius Chin",
    author_email="ignatius.chin@gmail.com",
    description="Package for extracting data from the Wholesale Electricity Market (WEM) of Western Australia and store in dataframe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igchin/WEMProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)