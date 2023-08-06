import os
from setuptools import setup, find_packages


def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            name, file_extension = os.path.splitext(filename)
            if file_extension == '.txt' or file_extension == '.yml' \
                    or filename == '.env' or name == 'Dockerfile':
                paths.append(os.path.join('..', path, filename))
    return paths


def package_all_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            if os.path.splitext(filename)[1] != '.local':
                paths.append(os.path.join('..', path, filename))
    return paths


all_files = package_files("langauge/")
ui = package_all_files("langauge/ui/")
db = package_all_files("langauge/core/database/init-db.d")


setup(
    name='langauge',
    version="0.0.3",
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={"langauge": all_files+ui+db},
    license='MIT',
    description="LanGauge: 'gauge' the usefulness of open-source medical datasets",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Flapmax',
    url='https://github.com/flapmx/LanGauge-INTERNAL',
    python_requires='>=3.6',
    keywords=['AI', 'NLP', 'Flapmax'],
    install_requires=[
        'click',
        'rapydo-controller'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        "console_scripts": [
            "langauge=langauge.cli:cli"
        ]
    }
)