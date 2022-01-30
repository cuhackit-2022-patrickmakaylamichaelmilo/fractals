from PIL import Image, ImageDraw, ImageFont
import math, colorsys, random
from typing import List
import functools


def linearVariation(x, y):
    return x, y


def sineVariation(x, y):
    return math.sin(x), math.sin(y)


def sphericalVariation(x, y):
    r = math.sqrt((x * x) + (y * y))
    return (1 / (r * r)) * x, (1 / (r * r)) * y


def horseshoeVariation(x, y):
    r = math.sqrt((x * x) + (y * y))
    return (1 / r) * (x - y) * (x + y), (2 * x * y) / r


def crossVariation(x, y):
    k = math.sqrt((1 / ((x * x - y * y) ** 2)))
    return k * x, k * y


def tangentVariation(x, y):
    return math.sin(x) / math.cos(y), math.tan(y)


funcMap = {
    "linearVariation": linearVariation,
    "sineVariation": sineVariation,
    "sphericalVariation": sphericalVariation,
    "horseshoeVariation": horseshoeVariation,
    "crossVariation": crossVariation,
    "tangentVariation": tangentVariation,
}


def theThingHelper(x1, y1, k, fun, mat):
    return fun(
        mat[k][0] * x1 + mat[k][1] * y1 + mat[k][2], mat[k][3] * x1 + mat[k][4] * y1 + mat[k][5]
    )


def canvasRescale(x, y, lb, ub):
    return ((x + 1) / 2) * 1000, abs(((-(y + 1) / 2) * 1000) + 1000)


def colorGrad(x, y, c1, c2):
    t = (x + y) / 2000
    return c2[0] + ((1 - t) * c1[0]), c2[1] + ((1 - t) * c1[1]), c2[2] + ((1 - t) * c1[2])


def generateFractal(
    a: float, b: float, c: float, c1: List[int], c2: List[int], funct: str
) -> Image:
    width, height = 1000, 1000
    img = Image.new("RGB", (width, height))

    fun = funcMap[funct]
    mat = ((c, 0, 0, 0, c, 0), (c, 0, a, 0, c, 0), (c, 0, 0, 0, c, b))

    doMirror = funct in [
        "sineVariation",
        "linearVariation",
        "sphericalVariation",
        "crossVariation",
        "tangentVariation",
    ]

    d = ImageDraw.Draw(img)

    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)

    for k in range(100000):
        i = random.randint(0, 2)
        x, y = theThingHelper(x, y, i, fun, mat)

        if k > 20:
            x1, y1 = canvasRescale(x, y, 1000, 1000)
            x2, y2 = canvasRescale(-x, y, 1000, 1000)
            x3, y3 = canvasRescale(x, -y, 1000, 1000)
            x4, y4 = canvasRescale(-x, -y, 1000, 1000)

            # t = (x1 + y1) / 2000

            cr, cg, cb = colorGrad(x1, y1, c1, c2)

            d.point((x1, y1), (int(cr), int(cg), int(cb), 255))

            if doMirror:
                cr, cg, cb = colorGrad(x2, y2, c1, c2)
                d.point((x2, y2), (int(cr), int(cg), int(cb), 255))
                cr, cg, cb = colorGrad(x3, y3, c1, c2)
                d.point((x3, y3), (int(cr), int(cg), int(cb), 255))
                cr, cg, cb = colorGrad(x4, y4, c1, c2)
                d.point((x4, y4), (int(cr), int(cg), int(cb), 255))

    return img


# basically if this file is being ran by itself, run the code in the if block
if __name__ == "__main__":
    generateFractal(0.5, 0.5, 0.5, [82, 45, 128], [245, 102, 0], "horseshoeVariation").show()
