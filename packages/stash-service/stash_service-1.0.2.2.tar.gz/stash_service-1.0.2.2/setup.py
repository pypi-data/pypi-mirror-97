from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='stash_service',
    version='1.0.2.2',
    description='A PyPI packages that supports all the necessary error codes, validation exception, common exceptions '
                'of a webservice. This PyPI package includes a method that establishes the connection to your '
                'firebase account.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['stash_service'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=['firebase-admin'],
    author='Maria Irudaya Regilan J, Venkateshwar S, D Vidhyalakshmi',
    author_email='britsa.tech@gmail.com'
)
