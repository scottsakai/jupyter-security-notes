from setuptools import setup

setup(
    name='sdsc_jupyter',
    version='0.1',
    description='SDSC JupyterHub Classes',
    packages=[
        'sdsc_jupyter',
        ],
    requires=['oauthenticator'],
    install_requires=['oauthenticator'],
    author='Rick Wagner',
    author_email='rick@ucsd.edu',
    maintainer_email='rick@ucsd.edu',
    license='BSD'
    )
