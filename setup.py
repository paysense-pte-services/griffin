from setuptools import setup

setup(
    name='griffin',
    version='1.0',
    description='Secret Management Library',
    url='https://github.com/paysense-pte-services/griffin',
    author='Supritha Krishnappa, Ritik Jain',
    author_email='supritha.krishnappa@payufin.com, ritik.jain@payufin.com',
    packages=['griffin'],
    zip_safe=False,
    install_requires=['hvac==1.0.0', 'redis>=3.4.1']
)
