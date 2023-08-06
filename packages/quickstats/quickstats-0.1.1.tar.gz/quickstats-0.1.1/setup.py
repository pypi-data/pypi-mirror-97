import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
VERSIONFILE="quickstats/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))    

setuptools.setup(
    name="quickstats", # Replace with your own username
    version=verstr,
    author="Alkaid Cheng",
    author_email="chi.lung.cheng@cern.ch",
    description="A tool for quick statistical analysis for HEP experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'quickstats':['macros/*.so','macros/*.pcm']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy'
      ],
    scripts=['bin/quickstats'],
    python_requires='>=3.7',
)
