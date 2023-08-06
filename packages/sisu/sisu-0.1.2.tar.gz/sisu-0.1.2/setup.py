#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['nltk', 'numpy', 'dill', 'gismo', 'scikit-network', 'matplotlib', 'PyQt5']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]


def _post_install():
    """Post installation nltk corpus downloads if nltk available."""
    import nltk
    import spacy
    spacy.cli.download('en_core_web_sm')
    nltk.download("punkt")
    nltk.download("stopwords")


class PostDevelop(develop):
    """Post-installation for development mode."""

    def run(self):
        develop.run(self)
        self.execute(_post_install, [], msg="Running post installation tasks")


class PostInstall(install):
    """Post-installation for production mode."""

    def run(self):
        install.run(self)
        self.execute(_post_install, [], msg="Running post installation tasks")


setup(
    author="Mélanie Cambus, Marc-Olivier Buob, Fabien Mathieu",
    author_email='fabien.mathieu@normalesup.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Performs extractive, hierarchical, summarization out of a corpus of documents.",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='sisu',
    name='sisu',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/balouf/sisu',
    version='0.1.2',
    zip_safe=False,
    cmdclass={"develop": PostDevelop, "install": PostInstall},
)
