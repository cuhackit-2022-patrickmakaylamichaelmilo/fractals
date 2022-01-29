from PIL import Image, ImageDraw, ImageFont
import math, colorsys, random
import io

def serpinskiTriangleHelper(x1, y1, i):
    if i == 0:
        return x1 / 2, y1 / 2
    elif i == 1:
        return (x1 + 1) / 2, y1 / 2
    elif i == 2:
        return x1 / 2, (y1 + 1) / 2

def serpinskiTriangle() -> bytes:
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
    
    image_data = io.BytesIO()
    img.save(image_data, "PNG")
    
    image_data.seek(0)
    return image_data

# basically if this file is being ran by itself, run the code in the if block
if __name__ == "__main__":
    image_data = serpinskiTriangle()
    Image.open(image_data).show("Serpinski Triangle")
    