from PIL import Image, ImageDraw, ImageFont
import math, colorsys, random

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

def theThingHelper(x1, y1, k, funct, a, b, c):
    mat = [[None, None, None, None, None, None], [None, None, None, None, None, None], [None, None, None, None, None, None]]
    mat = [[c, 0, 0, 0, c, 0], [c, 0, a, 0, c, 0], [c, 0, 0, 0, c, b]]
    s, t = 0, 0
    if funct == 'linearVariation':
        s += linearVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[0]
        t += linearVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[1]
    elif funct == 'sinVariation':
        s += sinVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[0]
        t += sinVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[1]
    elif funct == 'sphericalVariation':
        s += sphericalVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[0]
        t += sphericalVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[1]
    elif funct == 'horseshoeVariation':
        s += horseshoeVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[0]
        t += horseshoeVariation(mat[k][0]*x1 + mat[k][1]*y1 + mat[k][2], mat[k][3]*x1 + mat[k][4]*y1 + mat[k][5])[1]

    return s, t

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
            x1 = ((x + 1)/ 2) * 1000
            y1 = abs(((-(y + 1) / 2) * 1000) + 1000)
            t = (x1 + y1) / 2000
            cr = c2[0]+((1-t)*c1[0])
            cg = c2[1]+((1-t)*c1[1])
            cb = c2[2]+((1-t)*c1[2])
            d.point((x1, y1), (int(cr), int(cg), int(cb), 255))
    img.show()

theThing(0.5, 0.5, 0.5, [82, 45, 128], [245, 102, 0],  'horseshoeVariation')
