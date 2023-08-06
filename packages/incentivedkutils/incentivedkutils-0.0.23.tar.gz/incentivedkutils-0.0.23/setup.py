from setuptools import setup

with open('README.md', 'r') as fh:
    long_description=fh.read()


setup(
    name='incentivedkutils',
    version='0.0.23',
    description='Incentive utilities',
    py_modules=['incentivedkutils'],
    package_dir={'':'src'},
    install_requires=['tabulate'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Torben Franch',
    author_email='torben@franch.eu',

)