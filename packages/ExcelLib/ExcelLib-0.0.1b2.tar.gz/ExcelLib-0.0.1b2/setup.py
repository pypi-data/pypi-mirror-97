from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='ExcelLib',
    version='0.0.1b2',
    description='ChokChaisak',
    long_description=readme(),
    url='https://github.com/ChokChaisak/ChokChaisak',
    author='ChokChaisak',
    author_email='ChokChaisak@gmail.com',
    license='ChokChaisak',
    install_requires=[
        'pandas',
        'openpyxl',
        'xlsxwriter',
        'xlrd',
    ],
    keywords='ExcelLib',
    packages=['ExcelLib'],
    package_dir={
    'ExcelLib': 'src/ExcelLib',
    },
    package_data={
    'ExcelLib': ['*'],
    },
)