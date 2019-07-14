<table border=1>
  <tr>
    <td colspan=2><strong>Penrose</strong>&nbsp;&nbsp;&nbsp;&nbsp;
    <a href=#Screenshots>Screenshots</a> |
    <a href=#Features>Features</a> |
    <a href=#Resources>Resources</a> |
    <a href=#RunningTheCode>Running the Code</a>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/openscad.png style="width:50px"></td>
    <td>Experiments and demonstrations involving plane tilings, 3d solid geometry,
    Python, OpenSCAD, Houdini, Meshlab, etc</td>
  </tr>
</table>

<a name=References></a>
## References

#### Misc

* https://pypi.org/project/numpy-stl/
* https://github.com/phistrom/mesh2img

#### Houdini:

* https://github.com/kiryha/Houdini/wiki/python-for-artists
* https://github.com/kiryha/Houdini/wiki/python-snippets
* https://www.sidefx.com/docs/houdini/hom/hou/index.html (hpi reference)
* https://www.sidefx.com/tutorials/ (video tutorials)

#### Blender

* https://docs.blender.org/manual/en/latest/render/workflows/command_line.html

## Quick Start

```
## Prereqs:
## Make sure we can reach external tools.
echo "alias blender=/Applications/Blender/blender.app/Contents/MacOS/blender" >> ~/.bash_profile
echo "alias openscad=/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD" >> .bash_pofile
echo "export HBIN=/Applications/Houdini//Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/bin" >> .bash_profile'
echo "export PATH=${PATH}:/Applications/Houdini//Houdini17.5.293/Frameworks/Houdini.framework/Versions/Current/Resources/bin" >> .bash_profile'

## Bootstrap: (Note that houdini itself requires py2)
$ git clone --recursive  git@github.com:mattvonrocketstein/penrose.git
$ cd  penrose
$ mkvirtualenv  penrose --python python2
$ workon penrose
$ pip install -r requirements.txt
$ python setup.py develop

## Penrose Wrappers:
## simplify launching frameworks with penrose-as-library
## preconfigured, plus startup script
$ penrose houdini ./houdini/demo-1.py
$ penrose blender ./blender/demo-1.py
$ penrose meshlab ./meshlab/demo-1.py
$ penrose openscad ./blender/demo-1.py

# or equivalently
$ penrose hx ./houdini/demo-1.py
$ penrose bx ./blender/demo-1.py
$ penrose mx ./meshlab/demo-1.py
$ penrose scad ./openscad/demo-1.py
```

<a name=Screenshots></a>
## Screenshots

**3D tiling:**

<img src=img/screenshot2.png>

**3D top view detail:**

<img src=img/screenshot1.png>

**2D control**

<img src=img/cairo.png>

<a name=Features></a>
## Features

* Code generation of 3D scad instructions (via [solid](https://github.com/SolidCode/SolidPython) backend)
* Generation of triangle vertices corresponding to penrose tilings (in python)
* 2D rendering with [cairo backend](https://pypi.python.org/pypi/cairocffi)

<a name=Resources></a>
## Resources

* [Installing Python](https://www.python.org/downloads/)
* [Installing OpenSCAD](http://www.openscad.org/downloads.html)
* [Penrose tiling algorithm explanation](http://preshing.com/20110831/penrose-tiling-explained/)
* [OpenSCAD cheatsheet](http://www.openscad.org/cheatsheet/)
* [Solid docs](https://github.com/SolidCode/SolidPython)
* [OpenSCAD User Manual](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language)

<a name=RunningTheCode></a>
## Running the Code

Running the `penrose.py` script refreshes `penrose.scad` (3d backend) and `penrose.png` (2d backend).  More specifically:

```bash
alias openscad="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD" # for osx
python penrose.py
openscad penrose.scad
```
## Appendix

( originally from https://www.sidefx.com/forum/topic/43515/?page=1#post-223682 )

First thing, set your desktop to “Technical”. This gives you the folder view on the left hand side. A Houdini scene is actually composed of network folders and objects inside those networks. You can traverse these folders with the network pane.

Folders are associated with a network type. We have acronyms for the network types and the nodes inside these networks.

Object = Object type nodes in an Object type folder. These Object nodes allow you build transform constraint hierarchies. Geometry type Object nodes contain SOP nodes that construct and modify geometry that inherit any transforms at the object level.

SOPs = Surface OPerators or geometry nodes that are inside an object folder. These are used to construct and modify geometry. Any kind of geometry from polygons to volumes.

DOPs = Dynamic OPerators or simulation/solver nodes that are used to construct simulations. Simulations read in geometry from SOPs and passes this data in to the DOP solvers.

SHOP = SHading Operators are materials that represent a shader to apply to geometry. Some are hard coded with vex and others are folders that you can dive in to and modify the VOPs inside.

VOPs = Vector OPerators inside VOP network nodes are used for everything from building shaders to modifying geometry, volumes, pixels, and more.

VEX = Vector Expression Language. The code language used to write shaders. VOPs are wrappers around VEX code snippets.

CVEX = Context agnostic Vector Expression Language. This has replaced all the VEX specific contexts throughout Houdini. It is a generalized language that uses the same environment and functions anywhere inside Houdini.

COPs = Composite OPerators in composite type folders. Used in image compositing operations.

ROPs = Render OPerators in side ROP Output directories which are used to create render output dependency graphs for automating output of any type of data and for triggering external processes like rendering. Commonly used to generate sequences of geometry, simulation data and trigger Render tasks that generates sequences of images to disk.

CHOPs = CHannel OPerators used to create and modify any type of raw channel data from motion to audio and everything in between. Most users safely ignore the CHOP context, and so can you, for now. Put it on the “get to it later” list when learning Houdini. But definitely keep it on the list.



All these folder types and node types are clearly indicated inside the Tree View you get up by default with the Technical Desktop. I highly recommend anyone new to Houdini to get used to working with the Tree view as you can see everything in the scene without diving in and out all over the place.

What makes these acronyms so important is that you can communicate ideas much quicker without any ambiguity with your fellow Houdini co-workers. This is known as “Houdini Speak”.

We have stripped many acronyms from the docs but the fact that they still exist and get used all the time speaks volumes to their usefulness.
