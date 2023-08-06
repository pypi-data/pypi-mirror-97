This file is the README of the unit tests and example package of:
- The pypos3d library.
- The pypos3dv 3D OpenGL Viewer
- The LibreOffice based GUI

# 1. INTRODUCTION:
This library is a port of the old DATA3D library of the OpenSource Pojamas project.
I own both of them.

pypos3d aims to have a high level of quality.
Each version is automatically tested with a set of unit tests.
Coding rules are based on CNES (RNC-CNES-Q-HB-80-535) -CNES is the French National Space Agency-


# 2. INSTALLATION:

## Library Installation:
The library shall be installed with pip:
> python3 -m pip pypos3dtu

Each release of pypos3dtu shall test the same version of pypos3d library


## Configuration Management System:
The code is managed on SourceForge platform under SVN:
svn checkout svn://svn.code.sf.net/p/pojamas/svncode/ pojamas-svncode

Development and test files are gathered in directory **PyPoser**

This PyPoser directory contains an Eclipse/PyDev environment.


# 3. Tests:
Unit tests are delivered in this package (pypos3dtu)
This library is tested with unitest with a target coverage rate over 85%.

Installation and commissionning tests are performed on:
- CentOS 8, 7
- Fedora >30
- Microsoft Windows 10 
- Debian 10 (i386)


## Unit Tests:
To run the tests, 3 ways are available:

* Under Linux use script the _tu.sh_ to launch all tests:
 - Tests are run in parallel
 - Coverage Tests are run one by one (results in coverage\_results.txt)
 
 - Detailed logs are generated in directory: pypos3dtu/tulog
 - Results are generated in directory: pypos3dtu/tures

* Outside Linux (in non dev environments):
 - Locate the installation directory of pypos3dtu

   `> python -c "import pypos3dtu; print(pypos3dtu.__path__[0])"`
   
 - Change current directory to the previous value:
  
   `> cd C:\Users\olivier\AppData\Roaming\Python\Python38\site-packages\pypos3dtu`

 - Execute manually the tests

   `> python -m unittest discover -p "tu*.py"`

* In a development environment:
 - Checkout the Eclipse project (cf. link above)
 - Run tests from PyPoser/src/pypos3dtu
 - Don't forfget to clean the 'tures' directory before check-in


## Validation Tests:
Validation tests are 'free' tests excuted on the GUI (LibreOffice) and the viewer.
Validation tests of the viewer (pypos3dv command) shall be run on various hardware
platforms.

## Tests Platforms:

|Platform| CPU, RAM, GraphicCard | OS - Software |
|---------|----------------------|---------------|
|d16      | Intel Core) i7-7700HQ CPU @ 2.80GHz<br/><br/>x86\_64 - 4C/8T - RAM 16GB<br/>NVIDIA Corporation GP108M [GeForce MX150]|**CentOS 8 Stream**<br/>Python 3.6.8<br/>PyOpenGL 3.1.5<br/>Pillow 7.2|
|d6       | Intel Core) i5 CPU 750  @ 2.67GHz<br/><br/>x86\_64 - 4C/4T - RAM 4GB<br/>NVIDIA Corporation GF119 [GeForce GT 520]|**CentOS 7**<br/>Python 3.6.8<br/> Pillow 6.2 <br/>nvidia-390xx-390.138-1.el7.x86\_64<br/>PyOpenGL 3.1.5| 
|d8       | Intel Atom) CPU N2800   @ 1.86GHz<br/><br/> i386 - 2C/4T - RAM 4GB<br/>IGP 640MHz   | **Debian 10**<br/> Python 3.7.3<br/>Pillow 5.4.1<br/>PyGLM 1.99.3 <br/>PyOpenGL         3.1.5<br/>scipy            1.5.4<br/>numpy            1.19.4<br/>glfw             2.0.0<br/> xlrd             2.0.1<br/>|
|d10      | Intel Pentium dual-Core CPU E5300 @2.60GHz<br/><br/>x86\_64 - 2C/2T - RAM 6GB<br/>NVIDIA GeForce 8600 GT/PCIe/SSE2 256MB<br/>| **Microsoft Windows 10**<br/>Python 3.8.7<br/> Pillow     8.1.0<br/> PyGLM      1.99.3<br/> PyOpenGL   3.1.5<br/> glfw       2.0.0<br/> numpy      1.20.0<br/> Pillow     8.1.0<br/> pip        21.0.1<br/> scipy      1.6.0<br/> xlrd       2.0.1    |
|d9       | Intel Core i5<br/><br/>x86\_64 - 2C/4T - RAM 4GB<br/>IGP nnnMHz|**Fedora 33**|


# 5. Tests Data:
Units tests are using some tests data (geometries, textures, material libs, ...).
Tests data have been (usually) found on the web on: https://www.sharecg.com
They are all free and usable for this product (non-commercial use or totally free) 

In case of error on the license on embedded tests data, contact me. I'll fix it immediatly.

Included (partial) Open Source models:
 - https://www.sharecg.com/v/21521/gallery/11/Poser/Project-Human-Female
 - https://www.sharecg.com/v/44417/gallery/5/3D-Model/P-51D-Mustang
 - https://www.sharecg.com/v/86927/gallery/5/3D-Model/Hawker-Tempest-Mk5

 Many thanks to the contributors!

# LICENCE:
  This library and its unit tests are delivered under the BSD license.


KR, Olivier



