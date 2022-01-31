from pathlib import Path
from PIL import Image
import pygifsicle
import nimporter
import imageio
import time
import sys
import io
import os

# ensure modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from nimFractal import pyGenFractal

nimporter.build_nim_extensions(root=Path("../../"), danger=True)


def main():
    print("Generating gif...")

    start = time.time()
    frames = []

    for i in range(1, 101):
        print(f"Generating frame {i}/100...", end="\r")

        i /= 100

        frames.append(pyGenFractal(.36, i, .49, *[0, 8, 255], *[0, 255, 30], "horseshoeVariation", 141217))
    
    print()

    print("Saving...")

    frames = [Image.open(io.BytesIO(f)) for f in frames]
    frames += list(reversed(frames))

    with open("out.gif", "wb") as out_gif:
        imageio.mimwrite(out_gif, frames, format="gif", fps=30)

    print("Optimizing with gifsicle...")

    pygifsicle.optimize("out.gif")

    print(f"Finished generation in {round(time.time() - start)} seconds.")

if __name__ == "__main__":
    main()
