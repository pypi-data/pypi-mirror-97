#
# Change Log of pypos3d library
# 
# **SVN** : Refer to SVN database for details
#

0.4.0 (2021-02-17)
------------------
This version of this global project delivers an OpenGL 3D viewer for Wavefront files.
This viewer provides the means to observe geometries with simple coloring and texturing
capabilities.

Changes in pypos3d.wftk:
  - Class WFMat added to support simple viewer renderings
  - WaveGeom can read material files (.mtl)

Changes in pypos3d.pftk:
  - Poser customData management added for Figure, PoserMeshedObject


0.3.0 (2020-12-05)
------------------
New decimation function added. The package 'propslim' contains the port of the QSlim algorithm initially developed and distributed by Michael Garland in July 2004 within the "SlimKit Surface Modeling Tools".
This decimate function applies to "WaveGeom" and preserves 'texture' coordinates.

**WARNING**
Original copyrights and credentials are delivered within this independant module.
The original C++ code was GPL2. I don't know about my partial port, I suspect it to be _copylefted_ by it.
If it's not the case, I would choose for 'New BSD license'
For commercial usage in a closed source program, I suggest to remove the package: pypos3d.propslim

Other changes: Few new unit tests to foster relialability.


0.2.0 (2020-11-16)
------------------

Internal structure optim: (for a better code maintenability and few speed improvements)
- Do not differentiate Props and Actors in a Figure (do avoid some Misses)
- Delete class "channels" : Shall disappear after read, attributs inlined in PoserMeshedObject
- Delete Class "FigureDescription" --> inlined in Figure
- Delete class "AddChildSA" and "weld" and "linkParam"
- Add a consistency method on links

PoserFileParser refactoring:
  --> Read Speed x 6

Channel Cleaning Improved (and fixed)

New method (for pypos3dapp) : printChannelLinks

Take into account deformers : 
  waveDeformerProp
  coneForceField

And few bug fixes

0.1.8 (2020-11-04)
------------------
* valueOp computation enhancement to support all kind of operations (for ApplyDelta)
* Channels dependencies new algorithm (for pypos3dapp 0.2 needs)

0.1.7 (2020-10-23)
------------------
* Delivery error fixed (on setup.py and setup-tu.py)

0.1.6 (2020-10-22)
------------------
* First Release of pypos3d
* First Release of PyPos3dLO : The LibreOffice based GUI for pypos3d
* Langage support : Poser4 to Poser9


0.1.1 (2020-Oct)
----------------
  Test version (for PyPI and for the libreoffice application installer)


