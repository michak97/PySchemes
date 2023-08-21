import cv2 as cv
import numpy as np

from pathlib import Path
from schemeTool import ColorScheme, Color, random_color

import logging

logging.basicConfig(level=logging.DEBUG)

class DrawScheme():
    """
    Class to draw Color Scheme
    """

    def __init__(self, scheme: ColorScheme, size: tuple, path: Path):
        """
        Constructor
        :param scheme: Color Scheme to draw
        :param size: Size of image
        :param path: Path to save image
        """
        self.scheme:list[Color] = []
        self.size = size
        self.path = path
    
    def make_scheme(self, amount: int, darkMode: bool, color: Color):
        """
        Make a Scheme to draw
        """
        ct = ColorScheme(color, darkMode)
        ct.make_scheme(amount)
        self.scheme = ct.return_scheme()

    def draw(self):
        """
        Draw Color Scheme
        """
        # Create image
        img = np.zeros((self.size[0], self.size[1], 3), np.uint8)
        img.fill(255)
        # Draw colors
        for color in self.scheme:
            # Draw color
            img = cv.circle(img, (int(self.size[0]/2), int(self.size[1]/2)), int(self.size[0]/2), color.rgb, -1)
        cv.imwrite(str(self.path), img)

if __name__ == "__main__":
    # Create Color Scheme
    color = random_color()
    cl = ColorScheme(color, True)
    cl.make_scheme(5)
    # Create Draw Scheme
    ds = DrawScheme(cl, (500, 500), Path("test.png"))
    ds.draw()
