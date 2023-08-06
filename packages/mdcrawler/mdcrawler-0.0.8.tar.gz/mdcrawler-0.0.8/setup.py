import setuptools
from pathlib import Path

setuptools.setup(
    name="mdcrawler",
    version="0.0.8",
    packages=['mdcrawler','mdcrawler/model'],
    description=('Mildom(https://www.mildom.com/) crawler written in Python.'),
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license="MIT",
    maintainer="kthimuo",
    author='kthimuo',
    url='https://github.com/kthimuo/mildom-crawler',
    install_requires=[
        'requests>=2.21.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
