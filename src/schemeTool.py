import math
import random

""" Converts between hex, rgb, lch, and lab color formats
    Conversions and standard functions by CoPilot AI
    Color Scheming based on article by Lisa Charlotte Muth
"""

def hex2rgb(hex: str) -> tuple:
    """Converts a hex color string to an RGB tuple."""
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(rgb: tuple) -> str:
    """Converts an RGB tuple to a hex color string."""
    return '#%02x%02x%02x' % rgb

def hex2lch(hex: str) -> tuple:
    """Converts a hex color string to an LCH tuple."""
    return rgb2lch(hex2rgb(hex))

def lch2hex(lch: tuple) -> str:
    """Converts an LCH tuple to a hex color string."""
    return rgb2hex(lch2rgb(lch))

def lch2rgb(lch: tuple) -> tuple:
    """Converts an LCH tuple to an RGB tuple."""
    return lab2rgb(lch2lab(lch))

def rgb2lch(rgb: tuple) -> tuple:
    """Converts an RGB tuple to an LCH tuple."""
    return lab2lch(rgb2lab(rgb))

def lab2rgb(lab: tuple) -> tuple:
    """Converts an LAB tuple to an RGB tuple."""
    return xyz2rgb(lab2xyz(lab))

def rgb2lab(rgb: tuple) -> tuple:
    """Converts an RGB tuple to an LAB tuple."""
    return xyz2lab(rgb2xyz(rgb))

def xyz2rgb(xyz: tuple) -> tuple:
    """Converts an XYZ tuple to an RGB tuple."""
    return tuple(int(round(c * 255)) for c in xyz2rgb_float(xyz))

def xyz2rgb_float(xyz: tuple) -> tuple:
    """Converts an XYZ tuple to an RGB tuple of floats."""
    x, y, z = xyz
    r = x *  3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y *  1.8758 + z *  0.0415
    b = x *  0.0557 + y * -0.2040 + z *  1.0570
    r = 1.055 * math.pow(r, 1/2.4) - 0.055 if r > 0.0031308 else 12.92 * r
    g = 1.055 * math.pow(g, 1/2.4) - 0.055 if g > 0.0031308 else 12.92 * g
    b = 1.055 * math.pow(b, 1/2.4) - 0.055 if b > 0.0031308 else 12.92 * b
    return r, g, b

def rgb2xyz(rgb: tuple) -> tuple:
    """Converts an RGB tuple to an XYZ tuple."""
    return tuple(int(round(c * 255)) for c in rgb2xyz_float(rgb))

def rgb2xyz_float(rgb: tuple) -> tuple:
    """Converts an RGB tuple to an XYZ tuple of floats."""
    r, g, b = rgb
    r = math.pow((r + 0.055) / 1.055, 2.4) if r > 0.04045 else r / 12.92
    g = math.pow((g + 0.055) / 1.055, 2.4) if g > 0.04045 else g / 12.92
    b = math.pow((b + 0.055) / 1.055, 2.4) if b > 0.04045 else b / 12.92
    r *= 100
    g *= 100
    b *= 100
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    return x, y, z

def lab2xyz(lab: tuple) -> tuple:
    """Converts an LAB tuple to an XYZ tuple."""
    return tuple(int(round(c * 255)) for c in lab2xyz_float(lab))

def lab2xyz_float(lab: tuple) -> tuple:
    """Converts an LAB tuple to an XYZ tuple of floats."""
    l, a, b = lab
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200
    x = 0.95047 * math.pow(x, 3) if math.pow(x, 3) > 0.008856 else (x - 16/116) / 7.787
    y = 0.95047 * math.pow(y, 3) if math.pow(y, 3) > 0.008856 else (y - 16/116) / 7.787
    z = 0.95047 * math.pow(z, 3) if math.pow(z, 3) > 0.008856 else (z - 16/116) / 7.787
    return x, y, z

def xyz2lab(xyz: tuple) -> tuple:
    """Converts an XYZ tuple to an LAB tuple."""
    return tuple(int(round(c * 255)) for c in xyz2lab_float(xyz))

def xyz2lab_float(xyz: tuple) -> tuple:
    """Converts an XYZ tuple to an LAB tuple of floats."""
    x, y, z = xyz
    x /= 0.95047
    y /= 1.00000
    z /= 1.08883
    x = math.pow(x, 1/3) if x > 0.008856 else 7.787 * x + 16/116
    y = math.pow(y, 1/3) if y > 0.008856 else 7.787 * y + 16/116
    z = math.pow(z, 1/3) if z > 0.008856 else 7.787 * z + 16/116
    l = 116 * y - 16
    a = 500 * (x - y)
    b = 200 * (y - z)
    return l, a, b

def lab2lch(lab: tuple) -> tuple:
    """Converts an LAB tuple to an LCH tuple."""
    l, a, b = lab
    c = math.sqrt(a * a + b * b)
    h = math.atan2(b, a) * 180 / math.pi
    return l, c, h

def lch2lab(lch: tuple) -> tuple:
    """Converts an LCH tuple to an LAB tuple."""
    l, c, h = lch
    a = math.cos(h * math.pi / 180) * c
    b = math.sin(h * math.pi / 180) * c
    return l, a, b


class Color:
    """ Class that represents a color """
    def __init__(self, lightness: float, chroma: float, hue: float):
        self.lightness = lightness
        self.chroma = chroma
        self.hue = hue
        self.lch = (lightness, chroma, hue)
        self.lab = lch2lab(self.lch)
        self.xyz = lab2xyz(self.lab)
        self.rgb = xyz2rgb(self.xyz)
        self.hex = rgb2hex(self.rgb)
        self.saturation = self.chroma / 100

    def relative_luminance(self) -> float:
        """ Returns the relative luminance of the color."""
        return 0.2126 * self.rgb[0] + 0.7152 * self.rgb[1] + 0.0722 * self.rgb[2]

    def __str__(self) -> str:
        return self.hex

    def desaturate(self, amount: float):
        """ Returns a desaturated version of the color."""
        return Color(self.lightness, self.chroma * (1 - amount), self.hue)

    def saturate(self, amount: float):
        """ Returns a saturated version of the color."""
        return Color(self.lightness, self.chroma * (1 + amount), self.hue)

    def lighten(self, amount: float):
        """ Returns a lightened version of the color."""
        return Color(self.lightness * (1 + amount), self.chroma, self.hue)

    def darken(self, amount: float):
        """ Returns a darkened version of the color."""
        return Color(self.lightness * (1 - amount), self.chroma, self.hue)
    
    def hue_shift(self, amount: float):
        """ Returns a color with a shifted hue."""
        return Color(self.lightness, self.chroma, self.hue + amount)

def random_color() -> Color:
    """Returns a random color"""
    return Color(random.randint(0, 100), random.randint(0, 100), random.randint(0, 360))


class ColorScheme:
    """A color scheme object that can be used to generate a color scheme."""
    def __init__(self, base_color: Color, darkmode: bool = False) -> None:
        self.base_color:Color = base_color
        self.scheme:list[Color] = [base_color]
        self.darkmode:bool = darkmode
    
    def return_scheme(self) -> list[Color]:
        """Returns the color scheme."""
        return self.scheme

    def make_scheme(self, amount: int)-> None:
        """Generates a color scheme based on the base color."""
        scheme = self.scheme
        scheme.append(self.add_complementary_color(self.base_color))
        while len(scheme) < amount:
            scheme.append(self.add_neighboring_color(scheme[-1]))
            self.avoid_forest_green(scheme[-1])
            while self.too_close(scheme[-1], scheme[-2], 20):
                scheme[-1].hue_shift(random.randint(0, 15))
                scheme[-1].lighten(random.randint(-10, 10))
                scheme[-1].desaturate(random.randint(-10, 10))
            scheme.append(self.add_complementary_color(scheme[-1]))
        self.manage_saturation()
        self.manage_lightness()
        self.mixup_lightness()



    def add_neighboring_color(self, color: Color)-> Color:
        """ Adds a color to the scheme that is close to the base color."""
        return Color(color.lightness, color.chroma, (color.hue + 30) % 360)

    def add_complementary_color(self, color: Color) -> Color:
        """ Returns a color that is complementary to the base color."""
        return Color(color.lightness, color.chroma, (color.hue + 180) % 360)

    def euclidean_distance(self, color1: Color, color2: Color) -> float:
        """ Returns the euclidean distance between two colors."""
        return math.sqrt((color1.lightness - color2.lightness)**2 + (color1.chroma - color2.chroma)**2 + (color1.hue - color2.hue)**2)

    def too_close(self, color1: Color, color2: Color, threshold: float) -> bool:
        """ Returns true if the colors are too close together."""
        return self.euclidean_distance(color1, color2) < threshold

    def equalize_chroma(self):
        """ Returns a color with the same saturation as the base color."""
        for color in self.scheme:
            color.chroma = self.base_color.chroma

    def manage_saturation(self):
        for color in self.scheme:
            if color.lightness > 40:
                color.chroma = color.chroma * 0.5
            else:
                color.chroma = color.chroma * 1.5

    def manage_lightness(self):
        if self.darkmode:
            for color in self.scheme:
                color.lightness = 65
        else:
            for color in self.scheme:
                color.lightness = 35

    def mixup_lightness(self):
        for color in self.scheme:
            color.lightness = color.lightness + random.randint(-15, 15)

    def avoid_forest_green(self, color):
        """ Returns a color that is not forest green."""
        if 100 <= color.hue <= 130:
            color.hue=100
        elif 160 > color.hue > 130:
            color.hue=160
        return color

