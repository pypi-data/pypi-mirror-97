import ast
import os.path
import re

from setuptools import find_packages, setup


NAME = 'pax2graphml'
DESCRIPTION = 'A python library for large-scale regulation network analysis using BIOPAX and GRAPHML'
URL = 'https://gitlab.inria.fr/fmoreews/pax2graphml'
EMAIL = 'fjrmoreews@gmail.com'
AUTHOR = 'FJR Moreews'
REQUIRES_PYTHON = '>=3.6.0'





# What packages are required for this module to be executed?
REQUIRED = [
  'matplotlib','numpy','pandas','subprocrunner','lxml','pybiomart'
  #'graph_tool'
]

# What packages are optional?
EXTRAS = {
  'testing': ["pytest"]
}

def findVersion(pkname,srcfile):
 
    vers="0.0.0" 

    reg = re.compile(r'__version__\s*=\s*(.+)')
    with open(os.path.join(pkname, srcfile)) as f:
 
      for line in f:
        print(line) 
        m = reg.match(line)
        if m:
            vers = ast.literal_eval(m.group(1))
 
            break
    return vers


ldescription=open('README.md').read()

setup(
   name=NAME,
   version=findVersion(NAME, '__init__.py'),
   description=DESCRIPTION,
   long_description=ldescription,
   long_description_content_type='text/markdown',
   author=AUTHOR,
   author_email=EMAIL,
   url=URL,
#   packages=[NAME],
   packages=find_packages(exclude=['tests']),
   license='MIT',
   platforms="Posix; MacOS X;",
   classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
   zip_safe=False,
   package_dir={NAME:NAME}, #important 
   package_data={
      NAME: [
             
              'resources/*', NAME+'/resources/*',
              'data/*', NAME+'/data/*'
            ]
   },
   python_requires=REQUIRES_PYTHON,
   install_requires=REQUIRED,
   extras_require=EXTRAS,
)

 


 
