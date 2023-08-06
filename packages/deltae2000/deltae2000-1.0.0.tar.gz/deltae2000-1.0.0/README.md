deltae2000 is an implementation of the CIEDE2000 algorithm to calculate the perceptual
distance between two colours. This is implemented in pure Python with the intention to
run optimal on the PyPy interpreter.

See the [Wikipedia article](https://en.wikipedia.org/wiki/Color_difference#CIEDE2000) for
more information on the distance calculation.

Example usage:

```python
from deltae2000 import delta_e_cie2000
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor

delta_e_cie2000(
    convert_color(sRGBColor(255, 0, 0, is_upscaled=True), LabColor),
    convert_color(sRGBColor(125, 255, 125, is_upscaled=True), LabColor)
)
```

This is based on the implementation from [colormath](https://python-colormath.readthedocs.io)
which uses Numpy in the implementation. Use the colormath version if you are using the
CPython interpreter.
