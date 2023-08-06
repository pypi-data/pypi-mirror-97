import os
import re
import setuptools

with open(os.path.join("zm_au", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setuptools.setup(
    name="zm-au",
    version=version,
    author="Zeke Marffy",
    author_email="zmarffy@yahoo.com",
    packages=setuptools.find_packages(),
    url='https://github.com/zmarffy/au',
    license='MIT',
    description='auto-updater for programs',
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'packaging',
        'zetuptools>=3.0.0',
        'zmtools'
    ],
)
