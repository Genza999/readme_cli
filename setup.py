import io
import os
import re
import sys

from setuptools import find_packages
from setuptools import setup


if sys.version_info[:3] < (3, 0, 0):
    print("Requires Python 3 to run.")
    sys.exit(1)

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="read_me_cli",
    version="0.2.1",
    url="https://github.com/Genza999/readme_cli",
    license='MIT',

    author="Kisekka David",
    author_email="cartpix@gmail.com",

    description="Command line tool that displays github README.md content for github repositories",
    long_description=read("README.rst"),

    install_requires=[
        'beautifulsoup4==4.9.3',
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'idna==2.10',
        'requests==2.24.0',
        'soupsieve==2.0.1',
        'urllib3==1.25.10',
        'urwid==2.1.2'
    ],
    keywords='readme cli readme.md github repository',
    include_package_data=True,
    packages=["readme_cli"],
    entry_points={"console_scripts": ["readme_cli = readme_cli.main:main"]},
    python_requires=">=3",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
