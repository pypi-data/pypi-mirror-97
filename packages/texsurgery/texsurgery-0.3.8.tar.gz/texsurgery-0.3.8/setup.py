import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="texsurgery",
    version="0.3.8",
    author="Pablo Angulo, Juan Viu Sos, Miguel Angel Marco Buzunariz",
    author_email="pablo.angulo@upm.es",
    description="Replace some commands and environments within a TeX document by evaluating code inside a jupyter kernel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://framagit.org/pang/texsurgery",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      'jupyter_client',
    ],
    python_requires='>=3.6',
)
