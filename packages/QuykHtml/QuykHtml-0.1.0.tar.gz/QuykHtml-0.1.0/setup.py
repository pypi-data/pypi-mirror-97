import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QuykHtml", # Replace with your own username
    version="0.1.0",
    author="Marc D",
    author_email="marcwarrelldavis@yahoo.com",
    description="A python library that allows you to quickly and easily generate HTML templates and even create full-on websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwd1993/QuykHtml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)