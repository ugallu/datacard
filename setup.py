from setuptools import setup, find_packages

setup(
    name='datacard',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Kaggle-like dataset cards for pandas DataFrames',
    long_description=open('README.md').read(),
    install_requires=['plotly','IPython','pandas','numpy'],
    url='',
    author='Oláh István Gergely',
    author_email='olah.istvan.gergely@gmail.com'
)