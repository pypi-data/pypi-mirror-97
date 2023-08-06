import setuptools


with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xditya",
    version="0.0.1",
    author="Xditya",
    author_email="Jainamoswal4@gmail.com",
    description="Reserved for xditya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://xditya.me",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)