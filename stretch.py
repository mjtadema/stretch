#!/usr/bin/env python3
from PIL import Image

class Monitor:
    def __init__(self, w, h, voff = 0):
        self.w = w
        self.h = h
        self.voff = voff

        # Deal with offsets
        self.minh = round(0 + self.voff * self.h)
        self.maxh = round(self.h + self.voff * self.h)


class VirtualMonitor(list):
    def __init__(self, *mons, imsize = ()):
        super().__init__(mons)
        self.imsize = imsize

    def process(self):
        self.scale()
        self.translate()

    def translate(self):
        """
        Translate to fit scaled monitors in image
        :return: None
        """

        minh = self.minh()
        for mon in self:
            mon.maxh -= minh
            mon.minh -= minh

    def scale(self):
        """
        Scale the monitor dimensions to fit the image
        :param imsize: tuple
        :return: None
        """
        # Determine scaling factor
        # To fit child monitors in image
        imw, imh = self.imsize
        scaw = imw / self.totw()
        scah = imh / self.toth()
        sca = scaw * scah
        if sca > 1:
            sca = 1
        print(f"Scaling by {sca}")
        for mon in self:
            mon.w *= sca
            mon.maxh *= sca
            mon.minh *= sca

    def toth(self):
        return abs(self.maxh() - self.minh())

    def maxh(self):
        return max(mon.maxh for mon in self)

    def minh(self):
        return min(mon.minh for mon in self)

    def totw(self):
        return sum(mon.w for mon in self)

# everything relative to bottom
# first crop

def cropper(*mons, image = "test.jpg"):
    im = Image.open(image)
    mons = VirtualMonitor(*mons, imsize = im.size)

    mons.process()

    imw, imh = im.size

    print("imsize", im.size)


    """
        0
    0   ----
        |
        .
        .
        .
        ----
    """
    left = 0

    for i, mon in enumerate(mons):
        """
                    0
        0           ------
                    |
                    |
        imh - maxh  ------
                    |
                    .
                    .
                    .
        imh - minh  ------
                    |
                    |
        imh         ------
        """
        upper = imh - mon.maxh
        right = left + mon.w
        lower = imh - mon.minh

        print(mon.w, mon.h, mon.minh, mon.maxh)

        print(f"cropping {left} {upper} {right} {lower}")
        c = im.crop((left, upper, right, lower))
        fout = f"city_{i}.jpg"
        c.save(fout)
        print(f"Saved to {fout}")
        left += right

    print(f"Cropped {len(mons)} images")

cropper(
        Monitor(1366, 768, -0.5),
        Monitor(1920, 1080),
        Monitor(1440, 900)
)