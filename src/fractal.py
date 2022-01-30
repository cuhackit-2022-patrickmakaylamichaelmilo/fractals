# Michael & Makayla

from PIL import Image, ImageDraw, ImageFont
import math, colorsys, random

# def serpinskiTriangleHelper(x1, y1, i):
#     if i == 0:
#         return x1 / 2, y1 / 2
#     elif i == 1:
#         return (x1 + 1) / 2, y1 / 2
#     elif i == 2:
#         return x1 / 2, (y1 + 1) / 2
#
# def serpinskiTriangle():
#     width, height = 1000, 1000
#     img = Image.new('RGB', (width, height))
#     d = ImageDraw.Draw(img)
#     x = random.uniform(-1, 1)
#     y = random.uniform(-1, 1)
#
#     for k in range(100000):
#         i = random.randint(0, 2)
#         x, y = serpinskiTriangleHelper(x, y, i)
#         x, y = math.sin(x), math.sin(y)
#         # print(x, y)
#         if k > 20:
#
#             x1 = ((x + 1)/ 2) * 1000
#             y1 = abs(((-(y + 1) / 2) * 1000) + 1000)
#             # print(x1, y1)
#             d.point((x1, y1), (255, 0, 0, 255))
#     img.show()
#
# # serpinskiTriangle()
#
# # 3x6 matrix, generate random numbers between -10 10
#
#
# def identityVariationHelper(x1, y1, k):
#     mat = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]
#     c = 0.35
#     mat = [[c, 0, 0, 0, c, 0], [c, 0, 0.5, 0, c, 0], [c, 0, 0, 0, c, 0.5]]
#     # mat = [[0.85, 0.04, 0, -0.04, 0.85, 1.6], [0.2, -0.26, 0, 0.23, 0.22, 1.6], [-0.15, 0.28, 0, 0.26, 0.24, 0.44]]
#     # for i in range(3):
#         # for j in range(6):
#         #     mat[i][j] = random.uniform(-1, 1)
#     return mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5]
#
# def identityVariation():
#     width, height = 1000, 1000
#     img = Image.new('RGB', (width, height))
#     d = ImageDraw.Draw(img)
#     x = random.uniform(-1, 1)
#     y = random.uniform(-1, 1)
#
#     for k in range(100000):
#         i = random.randint(0, 2)
#         x, y = identityVariationHelper(x, y, i)
#         if k > 20:
#             x1 = ((x + 1)/ 2) * 1000
#             y1 = abs(((-(y + 1) / 2) * 1000) + 1000)
#             d.point((x1, y1), (255, 0, 255, 255))
#     img.show()
#
#

# identityVariation()


def linearVariation(x, y):
    return x, y

def sinVariation(x, y):
    return math.sin(x), math.sin(y)

def sphericalVariation(x, y):
    r = math.sqrt((x*x) + (y*y))
    return (1/(r*r))*x , (1/(r*r))*y

def horseshoeVariation(x, y):
    r = math.sqrt((x*x) + (y*y))
    return (1/r)*(x-y)*(x+y), (2*x*y)/r

def crossVariation(x, y):
    k = math.sqrt((1/((x*x - y*y)**2)))
    return k * x, k * y

def tangentVariation(x, y):
    return math.sin(x) / math.cos(y), math.tan(y)

def theThingHelper(x1, y1, k, funct, a, b, c):
    mat = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]
    mat = [[c, 0, 0, 0, c, 0], [c, 0, a, 0, c, 0], [c, 0, 0, 0, c, b]]
    s, t = 0, 0
    if funct == 'linearVariation':
        thing = linearVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])
        s += thing[0]
        t += thing[1]
    elif funct == 'sinVariation':
        thing = sinVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])
        s += thing[0]
        t += thing[1]
    elif funct == 'sphericalVariation':
        thing = sphericalVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])
        s += thing[0]
        t += thing[1]
    elif funct == 'horseshoeVariation':
        thing = horseshoeVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])
        s += thing[0]
        t += thing[1]
    elif funct == 'crossVariation':
        thing = crossVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])
        s += thing[0]
        t += thing[1]
    elif funct == 'tangentVariation':
        thing = tangentVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])
        s += thing[0]
        t += thing[1]

    return s, t

def canvasRescale(x, y, lb, ub):
    return ((x + 1)/ 2) * 1000, abs(((-(y + 1) / 2) * 1000) + 1000)

def colorGrad(x, y, c1, c2):
    t = (x + y) / 2000
    return c2[0]+((1-t)*c1[0]), c2[1]+((1-t)*c1[1]), c2[2]+((1-t)*c1[2])


def theThing(a, b, c, c1, c2, funct):
    width, height = 1000, 1000
    img = Image.new('RGB', (width, height))
    d = ImageDraw.Draw(img)
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    for k in range(100000):
        i = random.randint(0, 2)
        x, y = theThingHelper(x, y, i, funct, a, b, c)
        if k > 20:
            x1, y1 = canvasRescale(x, y, 1000, 1000)
            x2, y2 = canvasRescale(-x, y, 1000, 1000)
            x3, y3 = canvasRescale(x, -y, 1000, 1000)
            x4, y4 = canvasRescale(-x, -y, 1000, 1000)
            t = (x1 + y1) / 2000
            cr, cg, cb = colorGrad(x1, y1, c1, c2)
            d.point((x1, y1), (int(cr), int(cg), int(cb), 255))
            if funct == 'sphericalVariation':
                cr, cg, cb = colorGrad(x2, y2, c1, c2)
                d.point((x2, y2), (int(cr), int(cg), int(cb), 255))
                cr, cg, cb = colorGrad(x3, y3, c1, c2)
                d.point((x3, y3), (int(cr), int(cg), int(cb), 255))
                cr, cg, cb = colorGrad(x4, y4, c1, c2)
                d.point((x4, y4), (int(cr), int(cg), int(cb), 255))
    img.show()

theThing(0.5, 0.5, 0.5, [82, 45, 128], [245, 102, 0],  'sphericalVariation')


def theThing(a, b, c, c1, c2, funct):
    width, height = 1000, 1000
    img = Image.new('RGB', (width, height))
    d = ImageDraw.Draw(img)
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    for k in range(100000):
        i = random.randint(0, 2)
        x, y = theThingHelper(x, y, i, funct, a, b, c)
        if k > 20:
            x1, y1 = canvasRescale(x, y, 1000, 1000)
            x2, y2 = canvasRescale(-x, y, 1000, 1000)
            x3, y3 = canvasRescale(x, -y, 1000, 1000)
            x4, y4 = canvasRescale(-x, -y, 1000, 1000)

            # cr = c2[0]+((1-t)*c1[0])
            # cg = c2[1]+((1-t)*c1[1])
            # cb = c2[2]+((1-t)*c1[2])
            r,g,b = colorGrad(x1, y1, c1, c2)
            d.point((x1, y1), (int(r), int(g), int(b), 255))
            # if funct == 'sphericalVariation':
            #     r,g,b = colorGrad(x2, y2, c1, c2)
            #     d.point((x2, y2), (int(r), int(g), int(b), 255))
            #     r,g,b = colorGrad(x3, y3, c1, c2)
            #     d.point((x3, y3), (int(r), int(g), int(b), 255))
            #     r,g,b = colorGrad(x4, y4, c1, c2)
            #     d.point((x4, y4), (int(r), int(g), int(b), 255))
    img.show()








# spread = 17
# width, height = 1000, 800
# maxdepth = 12
# length = 8.0
#
#
# img = Image.new('RGB', (width, height))
# d = ImageDraw.Draw(img)
#
# def drawTree(x1, y1, angle, depth):
#     if depth > 0:
#         x2 = x1 + int(math.cos(math.radians(angle)) * depth * length)
#         y2 = y1 + int(math.sin(math.radians(angle)) * depth * length)
#
#         (r, g, b) = colorsys.hsv_to_rgb(float(depth) / maxdepth, 1.0, 1.0)
#         R, G, B = int(255 * r), int(255 * g), int(255 * b)
#
#         d.line([x1, y1, x2, y2], (R, G, B), depth)
#
#         drawTree(x2, y2, angle - spread, depth - 1)
#         drawTree(x2, y2, angle + spread, depth - 1)
#
# drawTree(width / 2, height * 0.9, -90, maxdepth)
# img.show()
# img.save("Tree.png", "PNG")
