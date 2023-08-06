from setuptools import find_packages, setup

version = '0.0.4'

setup(
    name='ctec-pytest-utils',
    version=version,
    packages=find_packages(),
    author='jjy',
    author_email='rxxy0101@163.com',
    url='http://www.189.cn',
    description='189 pytest utils',
    install_requires=['pytest>=4.6.11', 'pytest-html>=1.22.1', 'pytest-cov>=2.8.1', "flask>=0.10.1", "xlrd==1.2.0"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],

)
