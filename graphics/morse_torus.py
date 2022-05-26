#
# morse_torus.py
# --------------
#

import os
import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri


def generateTorus(theta, phi, a, b):
    x = (b + a * np.cos(theta)) * np.cos(phi)
    y = (b + a * np.cos(theta)) * np.sin(phi)
    z = a * np.sin(theta)

    return (x, y, z)

def generateSubspaces(args):
    num_pts = 200

    theta = np.linspace(0, 2*np.pi, num_pts)
    phi = np.linspace(0, 2*np.pi, num_pts)

    theta, phi = np.meshgrid(theta, phi)
    a = 1
    b = 2
    x, y, z = generateTorus(theta, phi, a, b)

    critical_points = [-b-a, -b+a, b-a, b+a]
    critical_point_labels = ['0', 'p_1', 'p_2', 'p_3']

    fig = plt.figure(figsize=(18,4))
    for i, critical_point in enumerate(critical_points):
        c = np.full(x.shape + (4,), [0, 0, 0, 0.1])  # shape (nx, ny, 4)
        c[y>critical_point, -1] = 0

        ax = fig.add_subplot(1, len(critical_points), i+1, projection='3d')
        ax.view_init(elev=0., azim=0)
        scale = 3.5
        ax.set_xlim3d([-scale, scale])
        ax.set_ylim3d([-scale, scale])
        ax.set_zlim3d([-scale, scale])

        ax.plot_surface(z, x, y, facecolors=c, rstride=2, cstride=2, edgecolors='w')
        ax.set_title("Subspace $f^{-1}" + f"(-\infty, {critical_point_labels[i]}]$")
    plt.savefig(os.path.join(args.path_to_output, f"torus.pdf"))
    # plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Draws Tori for Morse chapter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--path_to_output', type=str, help="Path to the output folder", required=True)
    args = parser.parse_args()
    generateSubspaces(args)
