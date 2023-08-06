import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ommtk",
    version="0.2.8",
    author="Gavin Bascom, Haotian Li, Janan Zhu",
    author_email="gavin@redesignscience.com",
    description="OpenMM Toolkit by Redesign Science",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedesignScience/RSSimTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
