from setuptools import setup

setup(
    name='griffin',
    version='1.3',
    description='Secret Management Library',
    url='https://github.com/paysense-pte-services/griffin',
    author='Supritha Krishnappa, Ritik Jain',
    author_email='supritha.krishnappa@payufin.com, ritik.jain@payufin.com',
    packages=['griffin'],
    zip_safe=False,
    install_requires=['hvac==0.7.1']
)
