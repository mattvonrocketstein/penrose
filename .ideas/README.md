<table border=1>
  <tr>
    <td colspan=2><strong><a href=https://github.com/mattvonrocketstein/penrose>Penrose</a></strong>&nbsp;&nbsp;&nbsp;&nbsp;
    </td>
  </tr>
  <tr>
    <td width=15%><img src=https://raw.githubusercontent.com/mattvonrocketstein/penrose/master/img/openscad.png style="width:50px"></td>
    <td>Experiments and demonstrations involving plane tilings, 3d solid geometry, Python and OpenSCAD</td>
  </tr>
</table>

## Index

* [Fibbonacci #1: Scale, Prune, Shift](#fibbonacci-1)
* [Accoustic panel](#acoustic-1)


<a name=acoustic-panel>

## Face slices as Acoustic Paneling


1. Slice a interesting face out of an object like one of these:

<a href=https://raw.githubusercontent.com/mattvonrocketstein/penrose/meshlab/img/screenshots/meshlab/snapshot00.png><img src=https://raw.githubusercontent.com/mattvonrocketstein/penrose/meshlab/img/screenshots/meshlab/snapshot00.png></a>

<a href=https://raw.githubusercontent.com/mattvonrocketstein/penrose/meshlab/img/screenshots/meshlab/snapshot01.png><img src=https://raw.githubusercontent.com/mattvonrocketstein/penrose/meshlab/img/screenshots/meshlab/snapshot01.png></a>

<a href=https://raw.githubusercontent.com/mattvonrocketstein/penrose/meshlab/img/screenshots/meshlab/snapshot02.png><img src=https://raw.githubusercontent.com/mattvonrocketstein/penrose/meshlab/img/screenshots/meshlab/snapshot02.png></a>

2. Save a suitable model for the slice, find vendor to laser cut the out of foam

<a name=fibbonacci-1>

## Fibbonacci #1: Scale, Prune, Shift


This describes a mobile / chandelier, or a heavy wall hanging of flat panels that project out into the Z axis

1. Pick any rectangle of the plane tiling below.  

2. Laser cut individual tiles at such a scale that the widest piece is 8 cm. Let this group of tiles be called a MODULE and suppose it is about 50 tiles total.

<a href=https://raw.githubusercontent.com/mattvonrocketstein/penrose/master/img/screenshot1.png><img src=https://raw.githubusercontent.com/mattvonrocketstein/penrose/master/img/screenshot1.png></a>

3. Repeat step #2 for 13 cm, then 21 cm, then 34 cm.  You now have 4 modules total, in increasingly large rectangular regions, each with their own tile-size.

4. Arrange modules 1,2,3,4 (corresponding to 8 cm, 13, 21, and 34 cm tiles respectively) front to back, where module 4 is furthest from the viewer.  

5. Let the distance from the viewer to module 4 be 3 meters.  Let the distance from the viewer to module 1 (smallest tiles) be 1 meter.  

6. Space modules 3 and module 2 evenly between modules 1 and 4.

7. For module 1 & 3, remove black tiles

8. For module 2 & 4 remove white tiles

9. Shift module 1 & 3 to the left by 5 cm.

10. Shift module 2 & 4 to the right by 5 cm.

11. For each tile in module 1, put 3cm of empty space between this tile and all other tiles.

12. Repeat for modules 2, 3, and 4.
