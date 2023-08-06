from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='basic physics formulas',
    version='1',
    description='this package having basic physics formulas',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['validate_mail'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",

        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    url="https://github.com/jasper22873/basic-physics-formulas",
    author='J.JASPER KIRUBAKARAN',
    author_email='jasper.kirubakaran@outlook.com'
)