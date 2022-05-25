#
# visualize.py
# ------------
# Visualizes Ising data files
# as tori.
#

import json
import argparse

import numpy as np
import matplotlib.pyplot as plt

from map_torus import map_image_to_torus

def main(args):
    img = np.load(args.path_to_file)
    print(np.min(img))
    a = 1.5
    b = 3
    torus = map_image_to_torus(img == -1, a, b)

    fig = plt.figure(figsize=(9,9))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter3D(torus[:, 0], torus[:, 1], torus[:, 2])
    ax.set_xlim([-b*2, b*2])
    ax.set_ylim([-b*2, b*2])
    ax.set_zlim([-b*2, b*2])
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualizes data as Tori.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--path_to_file', type=str, help="Path to the file.")
    args = parser.parse_args()
    main(args)
