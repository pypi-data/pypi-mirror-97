import re

from setuptools import find_packages, setup

from pathlib import Path


def read(filename):
    file_path = Path(__file__).parent / filename
    text_type = type(u"")
    with open(file_path, mode="r", encoding='utf-8') as f:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), f.read())


def get_requires():
    r_path = Path(__file__).parent / "requirements.txt"
    if r_path.exists():
        with open(r_path) as f:
            required = f.read().splitlines()
    else:
        requred = []

    r_path = Path(__file__).parent / "manual_requirements.txt"
    if r_path.exists():
        with open(r_path) as f:
            for req in f.read().splitlines():
                required.append(req)

    return required


setup(
    name="periodical_requests_recorder",
    version="0.2.4",
    url="https://github.com/fx-kirin/periodical_requests_recorder",
    license='MIT',

    author="fx-kirin",
    author_email="fx.kirin@gmail.com",

    description="",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),
    scripts=["scripts/periodical_recorder", ],

    install_requires=get_requires(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    data_files=[("", ["requirements.txt", "manual_requirements.txt"])],
)
