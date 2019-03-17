from setuptools import setup

setup(
    name='azorc',
    version='1.0',
    py_modules=['azorc.py'],
    include_package_data=True,
    install_requires=[
        'click',
        'pyfiglet'
    ],
    entry_points='''
        [console_scripts]
        azorc=azorc:cli
    ''',
)