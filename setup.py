from setuptools import setup, find_packages

setup(
    name='roastable',
    version='0.1',
    py_modules=['roastable'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ldap3',
    ],
    entry_points='''
        [console_scripts]
        roastable=roastable:main
    ''',
)
