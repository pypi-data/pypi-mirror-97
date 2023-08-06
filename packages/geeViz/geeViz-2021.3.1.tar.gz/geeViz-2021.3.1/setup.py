import setuptools
import re

try:
  from setuptools import setup                          
except ImportError:
  from distutils.core import setup                      
###################################################################
#Name Package
packages = ['geeViz']

#Provide what folders beyond the root of the package should be included in the package
package_data = {
        'geeViz': [
            'examples/*.py',
            'geeView/**',
             'geeView/**/**',
             'geeView/**/**/**'
        ],
    }
###################################################################
with open("README.md", "r") as fh:
    long_description = fh.read()
    
#GetVersion function taken from: https://github.com/google/earthengine-api/blob/master/python/setup.py
def GetVersion(package):
    print(package)
    with open(package+'/__init__.py') as f:
        return re.findall(r'__version__\s*=\s*\'([.\d]+)\'', f.read())[0]


setuptools.setup(
    name="geeViz",
    version= GetVersion(packages[0]),
    author="Ian Housman",
    author_email="ian.housman@gmail.com",
    description = 'A package to help with GEE data processing, analysis, and visualization',
    long_description=long_description,
    license='Apache',
    keywords='earthengine google remote sensing landsat sentinel modis forestry forest',
    long_description_content_type="text/markdown",
    url="https://ihousman@bitbucket.org/ihousman/geeViz",
    # packages=setuptools.find_packages(),
    packages=packages,
    package_data=package_data,
    
    classifiers=[
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta'
    ],
    install_requires=['earthengine-api','oauth2client'],
    # data_files = [('gee-py-viz',data_files)],

)