from setuptools import setup

setup(
    name='simple-text',
    version='0.1.0',
    packages=['dgsl_engine'],
    python_requires='>=3',
    description='A simple toy terminal text editor',
    url='https://github.com/strinsberg/simple-text',
    author='Steven Deutekom',
    entry_points = {
        'console_scripts': ['simple-text=simple-text.simple_text:main'],
    }
)
