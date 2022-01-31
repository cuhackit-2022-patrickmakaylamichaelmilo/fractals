import pygifsicle
import imageio
import time

from src_fractal import generateFractal

def main():
    print("Generating gif...")

    start = time.time()
    frames = []

    for i in range(1, 101):
        i /= 100

        frames.append(generateFractal(0.82, 0.83, i, [44, 84, 165], [28, 166, 150], "tangentVariation", 100000))

    frames = frames + list(reversed(frames))

    with open("out.gif", "wb") as out_gif:
        imageio.mimwrite(out_gif, frames, format="gif", fps=40)

    pygifsicle.optimize("out.gif")

    print(f"Finished generation in {round(time.time() - start)} seconds.")

if __name__ == "__main__":
    main()
