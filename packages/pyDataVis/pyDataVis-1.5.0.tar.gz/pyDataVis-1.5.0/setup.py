import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pyDataVis",
    version="1.5.0",
    description="A GUI application for fast visualization and analysis of numerical data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PierreAlphonse/pyDataVis.git",
    author="Pierre Alphonse",
    author_email="palphonse@wanadoo.fr",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scipy',
        'matplotlib',
        'PyQt5',
        'odfpy',
        'dans-diffraction'
    ],
    include_package_data=True,
    entry_points={
        "gui_scripts": [
            "pyDataVis=pyDataVis.main:run",
        ]
    },
)

