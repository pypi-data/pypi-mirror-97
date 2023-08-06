import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rockanalysis",
    version="0.1.1",
    author="Brandon Weindorf",
    author_email="bjweindorf@gmail.com",
    description="ROCK Data Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bweindorf/rockanalysis.git",
    install_requires=["matplotlib"],
    packages=['rockanalysis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
