import os
import re

import setuptools

with open(os.path.join("filemanips", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


setuptools.setup(
    name="filemanips",
    version=version,
    author="Zeke Marffy",
    author_email="zmarffy@yahoo.com",
    packages=setuptools.find_packages(),
    url='https://github.com/zmarffy/filemanips',
    license='MIT',
    description='File manipulation functions',
    python_requires='>=3.8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
