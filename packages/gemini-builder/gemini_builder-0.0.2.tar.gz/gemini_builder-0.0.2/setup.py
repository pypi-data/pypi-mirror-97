#! /usr/bin/python3
#

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setuptools.setup(name="gemini_builder",
      version="0.0.2",
      description="Build text/gemini files from Python",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Martin Ibert",
      author_email="python@maribert.info",
      license="MIT",
      packages=["gemini_builder"],
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires=">=3.7",
      zip_safe=True)