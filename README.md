# PYSCHEMES

** PySchemes is a package for generating color schemes. It includes functions for color conversion between HEX, RCB, LCH, XYZ and LAB.

## How to install this package:

`pip install pyschemes`

## How to use this package:

There are two main classes to this package, which are supposed to make working with colors easier. The main color form is LCH color, as it is a modern application of color, which is easy to use and is best for displaying colors in a way that's similar in how we humans perceive lightness and color in general. It's very easy to convert light and dark mode colors in LCH color space.

To define a color scheme, you initialize the ColorScheme class with a color. For this, you can either initialize a color class with an rgb string or use the random_color function. Optionally, you can define, whether you use a dark background or a light background, as it effects lightness and saturation of the color scheme.

Next, you use the make_scheme function of the ColorSheme class. Right now, the scheme generator only generates schemes by choosing neighboring colors. Support for monochromatic schemes and other schemes will be added soon.

The Scheme generator will try to avoid problems that define bad color schemes, though with time, more constraints might get added and others might be removed based on research.

## Included features:

- simple color and scheme generation
- conversion between color representations

## constraints

scheme generator will:

- try to avoid hues from all over the color wheel (use neighboring colors and their complements)
- mix up saturation and brightness
- avoid **green** green (leads to too similar colors)
- saturate dark, desaturate light 
- adapt to brightness of background

## Planned features:

- different scheme types
- better constraints
- add color blindness options
- adding opacity and string representations
- get a color scheme from an image

