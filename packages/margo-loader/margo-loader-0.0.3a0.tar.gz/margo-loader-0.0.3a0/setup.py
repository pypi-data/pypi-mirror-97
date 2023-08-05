import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'install-requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setuptools.setup(
    name="margo-loader", 
    version="0.0.3a0",
    author="Jake Kara",
    author_email="jake@jakekara.com",
    description="Import Jupyter notebooks using Margo notebook margin notebook syntax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakekara/nbdmod",
    packages=setuptools.find_packages(),
        entry_points = {
        'console_scripts': ['margo-tool=margo_loader.cli.__main__:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=read_requirements(),
    python_requires='>=3.6',
)
