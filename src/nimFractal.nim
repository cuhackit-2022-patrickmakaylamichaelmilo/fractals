{.checks: off, optimization: speed, passc: "-O3".}

import std/[math, random]
import nimpy
import pixie

randomize()

type
    Point {.shallow.} = tuple[x: float, y: float]

const
    RES = 1000

proc linearVariation(x: float, y: float): Point {.inline.} =
    return (x, y)

proc sineVariation(x: float, y: float): Point {.inline.} =
    return (sin(x), sin(y))

proc sphericalVariation(x: float, y: float): Point {.inline.} =
    let r2 = 1.0 / pow(sqrt(x * x + y * y), 2)
    return (r2 * x, r2 * y)

proc horseshoeVariation(x: float, y: float): Point {.inline.} =
    let r = sqrt((x * x) + (y * y))
    return ((1.0 / r) * (x - y) * (x + y), (2.0 * x * y) / r)

proc crossVariation(x: float, y: float): Point {.inline.} =
    let k = sqrt((1.0 / pow((x * x - y * y), 2)))
    return (k * x, k * y)

proc tangentVariation(x: float, y: float): Point {.inline.} =
    return (sin(x) / cos(y), tan(y))

proc canvasRescale(x: float, y: float): Point {.inline.} =
    return (((x + 1) / 2) * RES, abs(((-(y + 1) / 2) * RES) + RES))

proc colorGrad(x: float, y: float, c1: ColorRGB, c2: ColorRGB): ColorRGB {.inline.} =
    let t = 1.0 - ((x + y) / (RES.float * 2.0))

    return ColorRGB(
        r: uint8(min(c2.r.float + (t * c1.r.float), 255)),
        g: uint8(min(c2.g.float + (t * c1.g.float), 255)),
        b: uint8(min(c2.b.float + (t * c1.b.float), 255)),
    )

proc generateFractal(a: float, b: float, c: float, c1: ColorRGB, c2: ColorRGB, funct: string, iters: int): Image =
    let
        width, height = RES

        mat = [
            [c, 0, 0, 0, c, 0],
            [c, 0, a, 0, c, 0],
            [c, 0, 0, 0, c, b],
        ]

        doMirror = funct in [
            "sineVariation",
            "linearVariation",
            "sphericalVariation",
            "crossVariation",
            "tangentVariation",
            "hyperbolicVariation",
        ]
        
        fun = case funct:
            of "linearVariation": linearVariation
            of "sineVariation": sineVariation
            of "sphericalVariation": sphericalVariation
            of "horseshoeVariation": horseshoeVariation
            of "crossVariation": crossVariation
            of "tangentVariation": tangentVariation
            else: linearVariation
    
    var
        image = newImage(width, height)
        x = rand(2.0) - 1.0
        y = rand(2.0) - 1.0

    image.fill(color(0, 0, 0))

    for k in 0 .. iters-1:
        let
            i = rand(2)
            res = fun(mat[i][0] * x + mat[i][1] * y + mat[i][2], mat[i][3] * x + mat[i][4] * y + mat[i][5])

        x = res.x
        y = res.y

        if k > 20:
            let
                (x1, y1) = canvasRescale(x, y)

            image[x1.int, y1.int] = colorGrad(x1, y1, c1, c2)

            if doMirror:
                let
                    (x2, y2) = canvasRescale(-x, y)
                    (x3, y3) = canvasRescale(x, -y)
                    (x4, y4) = canvasRescale(-x, -y)

                image[x2.int, y2.int] = colorGrad(x2, y2, c1, c2)
                image[x3.int, y3.int] = colorGrad(x3, y3, c1, c2)
                image[x4.int, y4.int] = colorGrad(x4, y4, c1, c2)

    return image

proc pyGenFractal(a, b, c: float, cr1, cg1, cb1, cr2, cg2, cb2: int, funct: string, iters: int): string {.exportpy.} =
    let image = generateFractal(
        a,
        b,
        c,
        ColorRGB(r: cr1.uint8, g: cg1.uint8, b: cb1.uint8),
        ColorRGB(r: cr2.uint8, g: cg2.uint8, b: cb2.uint8),
        funct,
        iters
    )

    return image.encodeImage(FileFormat.ffPng)
