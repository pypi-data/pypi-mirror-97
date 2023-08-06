import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyvectors", # Replace with your own username
    version="1.0.2",
    author="Sjoerd Vermeulen",
    author_email="sjoerd@marsenaar.com",
    description="Introduces a new datatype called Vector for convinient working with vectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['vectors'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
