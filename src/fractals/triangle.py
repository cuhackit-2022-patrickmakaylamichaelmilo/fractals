from PIL import Image, ImageDraw, ImageFont
import math, colorsys, random


def serpinskiTriangleHelper(x1, y1, i):
    if i == 0:
        return x1 / 2, y1 / 2
    elif i == 1:
        return (x1 + 1) / 2, y1 / 2
    elif i == 2:
        return x1 / 2, (y1 + 1) / 2

def serpinskiTriangle() -> Image:
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

            x1 = ((x + 1)/ 2) * 1000 - 250
            y1 = abs(((-(y + 1) / 2) * 1000) + 1000) + 250
            # print(x1, y1)
            d.point((x1, y1), (255, 0, 0, 255))

    return img

# basically if this file is being ran by itself, run the code in the if block
if __name__ == "__main__":
    serpinskiTriangle().show()
    