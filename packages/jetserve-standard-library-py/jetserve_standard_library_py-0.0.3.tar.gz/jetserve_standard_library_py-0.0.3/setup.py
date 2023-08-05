"""
jetserve-standard-library-py packaging setup
"""
import io
import os
import re
import sys
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# sys.path.append(os.path.abspath(os.path.dirname(__file__))+'\\general')
sys.path.append(os.path.abspath(os.path.dirname(__file__))+'\\jetserve_standard_library_py')
# print(sys.path)

# import 'jetserve-standard-library-py' as cur

from setuptools import setup, find_packages
from jetserve_standard_library_py.general.version import VERSION
# print(VERSION)

# def read(*names, **kwargs):
#     with io.open(
#         os.path.join(os.path.dirname(__file__), *names),
#         encoding=kwargs.get('encoding', 'utf8')
#     ) as fp:
#         return fp.read()
#
#
# def find_version(*file_paths):
#     version_file = read(*file_paths)
#     version_match = re.search(
#         r'^__version__ = [\'"]([^\'"]*)[\'"]', version_file, re.M)
#     if version_match:
#         return version_match.group(1)
#     raise RuntimeError('setup ERROR : cannot specify VERSION')


tests_require = [
    # 'coverage',
    # 'pep8',
    # 'pyflakes',
    # 'pylint',
    # 'pytest',
    # 'pytest-cov',
    # 'pytest-xdist',
]

dev_require = [
    # 'ipdb',
    # 'ipython',
]

docs_require = [
    # 'recommonmark>=0.4.0',
    # 'Sphinx>=1.3.5',
    # 'sphinxcontrib-napoleon>=0.4.4',
    # 'sphinx-rtd-theme>=0.1.9',
]


setup(
    name='jetserve_standard_library_py',
    version=VERSION,
    description='jetserve_standard_library_py is IN-HOUSE python standard library for jetserve development team.'\
                '(team 1)',
    long_description=__doc__,
    url='https://github.com/jetserve-tso/jetserve-standard-library-py.git',
    author='Tae-Sun Oh, In-Jin Whoang',
    author_email='ohts@jetserve.net',
    license='MIT License',
    zip_safe=True,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Natural Language :: Korean',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Capture',
    ],

    packages=find_packages(),

    setup_requires=[
        'pytest-runner',
    ],
    install_requires=[
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'dev':  dev_require + tests_require + docs_require,
        'docs':  docs_require,
    },
)
