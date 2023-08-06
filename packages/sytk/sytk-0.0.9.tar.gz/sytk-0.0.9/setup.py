import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sytk",
    version="0.0.9",
    author="universuen",
    author_email="universuen@gmail.com",
    description="Some tools making life a little easier :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/universuen/sytk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)