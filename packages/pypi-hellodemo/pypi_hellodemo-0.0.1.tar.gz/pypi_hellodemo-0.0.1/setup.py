from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: MacOS :: MacOS X"
]

setup(
    name='pypi_hellodemo',      #same name as PACK_DIR (see intructions.txt)
    version='0.0.1',
    description='greeting package',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Jesse DeSimone, Ph.D.',
    author_email='desimone.neuro@gmail.com',
    classifers=classifiers,
    keywords='greeting',
    packages=find_packages(),
    install_requires=[]
)
