# Copyright 2012-2015, 2017, 2019-2021 Richard Dymond (rjdymond@gmail.com)
#
# This file is part of SkoolKit.
#
# SkoolKit is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# SkoolKit is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# SkoolKit. If not, see <http://www.gnu.org/licenses/>.

from skoolkit.pngwriter import PngWriter

TRANSPARENT = 'TRANSPARENT'
BLACK = 'BLACK'
BLUE = 'BLUE'
RED = 'RED'
MAGENTA = 'MAGENTA'
GREEN = 'GREEN'
CYAN = 'CYAN'
YELLOW = 'YELLOW'
WHITE = 'WHITE'
BRIGHT_BLUE = 'BRIGHT_BLUE'
BRIGHT_RED = 'BRIGHT_RED'
BRIGHT_MAGENTA = 'BRIGHT_MAGENTA'
BRIGHT_GREEN = 'BRIGHT_GREEN'
BRIGHT_CYAN = 'BRIGHT_CYAN'
BRIGHT_YELLOW = 'BRIGHT_YELLOW'
BRIGHT_WHITE = 'BRIGHT_WHITE'

PNG_ALPHA = 'PNGAlpha'
PNG_COMPRESSION_LEVEL = 'PNGCompressionLevel'
PNG_ENABLE_ANIMATION = 'PNGEnableAnimation'

class ImageWriter:
    """Initialise the image writer.

    :param config: A dictionary constructed from the contents of the
                   :ref:`ref-ImageWriter` section of the ref file.
    :param palette: A dictionary constructed from the contents of the
                    :ref:`ref-Colours` section of the ref file. Each key is a
                    colour name, and each value is a three-element tuple
                    representing an RGB triplet.

    If `config` or `palette` is `None`, empty, or missing values, default
    values are used.
    """
    # Component API
    def __init__(self, config=None, palette=None):
        self.options = self._get_default_options()
        if config:
            for k, v in config.items():
                try:
                    self.options[k] = int(v)
                except ValueError:
                    pass
        default_colours = self.get_default_colours()
        full_palette = dict(default_colours)
        if palette:
            full_palette.update(palette)
        self.colours = tuple(full_palette[c[0]] for c in default_colours)
        self.attr_index = self.get_attr_map()
        self.masks = {
            0: NoMask(),
            1: OrAndMask(),
            2: AndOrMask()
        }
        self.writer = PngWriter(self.options[PNG_ALPHA] & 255, self.options[PNG_COMPRESSION_LEVEL], self.masks)

    # Component API
    def image_fname(self, fname):
        """
        Convert the `fname` parameter of an image macro into an image filename
        with an appropriate extension.

        :param fname: The `fname` parameter of the image macro.
        :return: The image filename.
        """
        if fname.lower()[-4:] != '.png':
            return fname + '.png'
        return fname

    # Component API
    def write_image(self, frames, img_file):
        """
        Write an image file. If this method leaves the image file empty, the
        file will be removed.

        :param frames: A list of :class:`~skoolkit.graphics.Frame` objects from
                       which to build the image.
        :param img_file: The file object to write the image to.
        :return: The content with which the image macro is replaced; if `None`,
                 an appropriate ``<img .../>`` element is used.
        """
        use_flash = len(frames) == 1 and self.options[PNG_ENABLE_ANIMATION]
        attrs = set()
        colours = set()
        has_trans = False
        for frame in frames:
            if not hasattr(frame, 'colours'):
                self._get_colours(frame, use_flash)
            colours.update(frame.colours)
            attrs.update(frame.attrs)
            has_trans = has_trans or frame.has_trans
        palette, attr_map, has_trans = self._get_palette(colours, attrs, has_trans, frames[0].tindex)
        self.writer.write_image(frames, img_file, palette, attr_map, has_trans, frames[0].flash_rect)

    def get_default_colours(self):
        return (
            (TRANSPARENT, (0, 254, 0)),
            (BLACK, (0, 0, 0)),
            (BLUE, (0, 0, 197)),
            (RED, (197, 0, 0)),
            (MAGENTA, (197, 0, 197)),
            (GREEN, (0, 198, 0)),
            (CYAN, (0, 198, 197)),
            (YELLOW, (197, 198, 0)),
            (WHITE, (205, 198, 205)),
            (BRIGHT_BLUE, (0, 0, 255)),
            (BRIGHT_RED, (255, 0, 0)),
            (BRIGHT_MAGENTA, (255, 0, 255)),
            (BRIGHT_GREEN, (0, 255, 0)),
            (BRIGHT_CYAN, (0, 255, 255)),
            (BRIGHT_YELLOW, (255, 255, 0)),
            (BRIGHT_WHITE, (255, 255, 255))
        )

    def _get_default_options(self):
        return {
            PNG_COMPRESSION_LEVEL: 9,
            PNG_ENABLE_ANIMATION: 1,
            PNG_ALPHA: 255
        }

    def get_attr_map(self):
        attr_map = {}
        for attr in range(256):
            if attr & 64:
                ink = 8 + (attr & 7)
                paper = 8 + (attr & 56) // 8
                if ink == 8:
                    ink = 1
                if paper == 8:
                    paper = 1
            else:
                ink = 1 + (attr & 7)
                paper = 1 + (attr & 56) // 8
            attr_map[attr] = (paper, ink)
        return attr_map

    def _check_pixels(self, colours, pixels, ink, paper, has_trans, has_non_trans):
        if ink in pixels:
            colours.add(ink)
            has_non_trans = True
        if paper in pixels:
            colours.add(paper)
            has_non_trans = True
        return has_trans or None in pixels, has_non_trans

    def _get_colours(self, frame, use_flash=False):
        udg_array = frame.udgs
        null_mask = frame.mask == 0
        scale = frame.scale
        mask = self.masks[frame.mask]
        x0, y0, width, height = frame.x, frame.y, frame.width, frame.height
        x1, y1 = x0 + width, y0 + height
        attrs = set()
        colours = set()
        has_masks = 0
        has_trans = False
        flashing = False
        inc = 8 * scale
        min_col, max_col = x0 // inc, x1 // inc
        min_row, max_row = y0 // inc, y1 // inc
        x0_floor, x1_floor = inc * min_col, inc * max_col
        y0_floor, y1_floor = inc * min_row, inc * max_row
        min_x, min_y = width, height
        max_x = max_y = 0

        y = y0_floor
        for row in udg_array[min_row:max_row + 1]:
            x = x0_floor
            for udg in row[min_col:max_col + 1]:
                attr = udg.attr
                attrs.add(attr)
                paper, ink = self.attr_index[attr]
                if udg.mask:
                    has_masks = 1
                udg_whole = x0 <= x < x1_floor and y0 <= y < y1_floor
                has_non_trans = False
                if udg_whole:
                    # Uncropped UDG
                    for i in range(8):
                        pixels = mask.apply(udg, i, paper, ink, None)
                        has_trans, has_non_trans = self._check_pixels(colours, pixels, ink, paper, has_trans, has_non_trans)
                        if ink in colours and paper in colours and has_non_trans and (null_mask or has_trans):
                            break
                else:
                    # Cropped UDG
                    min_k = max(0, (x0 - x) // scale)
                    max_k = min(8, 1 + (x1 - 1 - x) // scale)
                    min_j = max(0, (y0 - y) // scale)
                    max_j = min(8, 1 + (y1 - 1 - y) // scale)
                    for j in range(min_j, max_j):
                        pixels = mask.apply(udg, j, paper, ink, None)[min_k:max_k]
                        has_trans, has_non_trans = self._check_pixels(colours, pixels, ink, paper, has_trans, has_non_trans)
                        if ink in colours and paper in colours and has_non_trans and (null_mask or has_trans):
                            break
                if use_flash and attr & 128 and ink != paper and has_non_trans:
                    if udg_whole:
                        min_x = min(x, min_x)
                        max_x = max(x + inc, max_x)
                        min_y = min(y, min_y)
                        max_y = max(y + inc, max_y)
                    else:
                        fx0 = max(x0, x + min_k * scale)
                        fx1 = min(x1, x + max_k * scale)
                        fy0 = max(y0, y + min_j * scale)
                        fy1 = min(y1, y + max_j * scale)
                        min_x = min(fx0, min_x)
                        max_x = max(fx1, max_x)
                        min_y = min(fy0, min_y)
                        max_y = max(fy1, max_y)
                    flashing = True
                    colours.add(ink)
                    colours.add(paper)
                x += inc
            y += inc

        if flashing:
            frame.flash_rect = (min_x - x0, min_y - y0, max_x - min_x, max_y - min_y)
        else:
            frame.flash_rect = None
        frame.has_trans = has_trans
        frame.has_masks = has_masks
        frame.colours = colours
        frame.attrs = attrs

    def _get_palette(self, colours, attrs, has_trans, tindex):
        colour_map = {}
        palette = []
        i = 0
        if has_trans:
            palette.extend(self.colours[0])
            i += 1
        elif tindex in colours:
            palette.extend(self.colours[tindex])
            colours.remove(tindex)
            has_trans = True
            i += 1
        for colour in colours:
            palette.extend(self.colours[colour])
            colour_map[colour] = i
            i += 1

        attr_map = {}
        for attr in attrs:
            paper, ink = self.attr_index[attr]
            attr_map[attr] = (colour_map.get(paper, 0), colour_map.get(ink, 0))

        return palette, attr_map, has_trans

class NoMask:
    def apply(self, udg, row, paper, ink, trans):
        udg_byte = udg.data[row]
        pixels = [paper] * 8
        index = 7
        while udg_byte:
            if udg_byte & 1:
                pixels[index] = ink
            udg_byte //= 2
            index -= 1
        return pixels

class OrAndMask:
    def apply(self, udg, row, paper, ink, trans):
        udg_byte = udg.data[row]
        if udg.mask:
            mask_byte = udg.mask[row]
        else:
            mask_byte = udg_byte
        pixels = [paper] * 8
        index = 7
        while mask_byte:
            if mask_byte & 1:
                if udg_byte & 1:
                    pixels[index] = ink
                else:
                    pixels[index] = trans
            udg_byte //= 2
            mask_byte //= 2
            index -= 1
        return pixels

    def colours(self, patterns, paper, ink, trans):
        return (
            patterns[paper], # 00
            patterns[trans], # 01
            patterns[paper], # 10
            patterns[ink]    # 11
        )

class AndOrMask:
    def apply(self, udg, row, paper, ink, trans):
        udg_byte = udg.data[row]
        if udg.mask:
            mask_byte = udg.mask[row]
        else:
            mask_byte = udg_byte
        pixels = [paper] * 8
        index = 7
        while udg_byte or mask_byte:
            if udg_byte & 1:
                pixels[index] = ink
            elif mask_byte & 1:
                pixels[index] = trans
            udg_byte //= 2
            mask_byte //= 2
            index -= 1
        return pixels

    def colours(self, patterns, paper, ink, trans):
        return (
            patterns[paper], # 00
            patterns[trans], # 01
            patterns[ink],   # 10
            patterns[ink]    # 11
        )
