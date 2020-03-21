from setuptools import setup

setup(
    name='dockerize',
    version='0.1',
    py_modules=['dockerize'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        dockerize=dockerize:cli
    ''',
)