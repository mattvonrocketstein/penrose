<table border=1>
  <tr>
    <td colspan=2><strong>Penrose</strong>&nbsp;&nbsp;&nbsp;&nbsp;
    <a href=#screenshots>Screenshots</a> |
    <a href=#features>Features</a> |
    <a href=#resources>Resources</a> |
    <a href=#running-the-code>Running the Code</a>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/openscad.png style="width:50px"></td>
    <td>Experiments and demonstrations involving plane tilings, 3d solid geometry, Python and OpenSCAD</td>
  </tr>
</table>

## Screenshots

**3D tiling:**

<img src=img/screenshot2.png>

**3D top view detail:**

<img src=img/screenshot1.png>

**2D control**

<img src=img/cairo.png>

## Features

* Code generation of 3D scad instructions (via [solid](https://github.com/SolidCode/SolidPython) backend)
* Generation of triangle vertices corresponding to penrose tilings (in python)
* 2D rendering with [cairo backend](https://pypi.python.org/pypi/cairocffi)

## Resources

* [Installing Python](https://www.python.org/downloads/)
* [Installing OpenSCAD](http://www.openscad.org/downloads.html)
* [Penrose tiling algorithm explanation](http://preshing.com/20110831/penrose-tiling-explained/)
* [OpenSCAD cheatsheet](http://www.openscad.org/cheatsheet/)
* [Solid docs](https://github.com/SolidCode/SolidPython)

## Running the Code

Running the `penrose.py` script refreshes `penrose.scad` (3d backend) and `penrose.png` (2d backend).  More specifically:

```bash
alias openscad="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD" # for osx
python penrose.py
openscad penrose.scad
```
