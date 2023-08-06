# Shape4D

## About Shape4D

Shape4D is a small library for one to create a 3D body in a scripting way, which is visible on demand during scripting.

## Core Features
- Shapes: Point, segment and Polygon.
- Visual Functions : a.plot(), a.add_plot(b), a.show().
- Creating a polyhedron by changing shapes to desire positions.
- When a 3D Polygon intercepts a 3D line, a point will be visble on the polygon, but no line is visible, due to the limitation in shading of matplotlib. 
- `__contains__`, overloaded for point in segment and polygon.
- `__hash__` and `__eq__`, overloaded for point, segment and polygon.
- `__neg__` overloaded for polygon.

The strategy to make entities visible is learnt from [pyny3d](https://pypi.org/project/pyny3d/) that is specific for convex polygons.  

At present, the engine is matplotlib, not ready for others, such as [open3D](http://www.open3d.org/), sketchup, abd Blender.

## Requirements

* [Python](http://www.python.org) 3 
* Matplotlib is needed.

## Documentation

To be continued.

## Installation
```bash
pip install Shape4D
```

## Usage

See Documentations

## Change Log

[changelog.md](changelog.md)

## License

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contact
heliqun@ustc.edu.cn

