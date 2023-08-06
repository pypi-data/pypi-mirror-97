
from setuptools import setup, find_packages

__version__ = ""
exec(open('goodok_mlu/version.py').read())


setup(
    name='goodok_mlu',
    version=__version__,
    description='Common ML utils',
    author='Alexey U. Gudchenko',
    author_email='proga@goodok.ru',
    url='https://github.com/goodok/ml_utils',
    packages=find_packages(),
    python_requires='>=3.6',
)
