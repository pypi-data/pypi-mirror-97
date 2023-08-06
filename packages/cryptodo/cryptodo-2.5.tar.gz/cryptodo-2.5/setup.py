from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.5'
DESCRIPTION = 'TEXT ENCRYPTION AND DECRYPTION'
LONG_DESCRIPTION = 'CRYPTODO'

# Setting up
setup(
    name="cryptodo",
    version=VERSION,
    author="k.a.ishan oshada",
    author_email="<ic31908@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    keywords=['encrypt()','decrypt()'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)