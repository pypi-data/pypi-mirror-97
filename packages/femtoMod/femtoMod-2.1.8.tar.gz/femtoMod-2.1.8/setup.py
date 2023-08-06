import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="femtoMod",
    version="2.1.8",
    author="Patrick, Benjamin, Etienne",
    description="femtoQ Modules",
    long_description=long_description,
    url="https://github.com/UltraFastQ/Modules",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
