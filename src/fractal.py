# Michael & Makayla

from PIL import Image, ImageDraw, ImageFont
import math, colorsys, random

def serpinskiTriangleHelper(x1, y1, i):
    if i == 0:
        return x1 / 2, y1 / 2
    elif i == 1:
        return (x1 + 1) / 2, y1 / 2
    elif i == 2:
        return x1 / 2, (y1 + 1) / 2

def serpinskiTriangle():
    width, height = 1000, 1000
    img = Image.new('RGB', (width, height))
    d = ImageDraw.Draw(img)
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)

    for k in range(100000):
        i = random.randint(0, 2)
        x, y = serpinskiTriangleHelper(x, y, i)
        # print(x, y)
        if k > 20:

            x1 = ((x + 1)/ 2) * 1000
            y1 = abs(((-(y + 1) / 2) * 1000) + 1000)
            # print(x1, y1)
            d.point((x1, y1), (255, 0, 0, 255))
    img.show()

serpinskiTriangle()

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
