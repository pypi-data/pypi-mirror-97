import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stockpriceanna",
    version="1.2.3",
    author="DrEdwC",
    author_email="edwincca@hotmail.com",
    description="a collect of tools for analyzing stock prices",
    long_description="a collect of tools for analyzing stock prices",
    long_description_content_type="text/markdown",
    url="https://github.com/edwincca/stockpriceanna/blob/master/README.md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)