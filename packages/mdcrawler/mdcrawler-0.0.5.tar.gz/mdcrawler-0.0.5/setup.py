from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import setup
from setuptools import find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="mdcrawler",
    version="0.0.5",
    description="Mildom(https://www.mildom.com/) crawler written in Python",
    author="kthimuo",
    url="https://github.com/kthimuo/mildom-crawler",
    packages=find_packages("mdcrawler"),
    package_dir={"": "mdcrawler"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt')
)

