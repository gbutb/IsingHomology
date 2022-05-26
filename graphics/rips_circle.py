#
# rips_cicle.py
# -------------
# Generates Rips complex
# for a points on S^1
#

import os
import argparse

import numpy as np
import dionysus as d

import matplotlib.pyplot as plt


def main(args):
    radius = args.radius
    theta = np.linspace(0, 2*np.pi, args.num_points)
    epsilon = np.random.uniform(-args.epsilon, args.epsilon, (args.num_points, 2))
    x = radius*np.cos(theta) + epsilon[:, 0]
    y = radius*np.sin(theta) + epsilon[:, 1]

    points = np.asarray([x,y])
    points = np.einsum("ab->ba", points)

    # Construct rips complex
    f = d.fill_rips(points, 2, args.delta)

    vertices = []
    edges = []
    faces = []
    for simplex in f:
        if simplex.dimension() == 0:
            vertices.append(points[simplex[0]])
        elif simplex.dimension() == 1:
            edges.append([points[simplex[0]], points[simplex[1]]])
        elif simplex.dimension() == 2:
            faces.append([points[simplex[0]], points[simplex[1]], points[simplex[2]]])

    vertices = np.asarray(vertices)
    edges = np.asarray(edges)
    faces = np.asarray(faces)

    plt.figure(figsize = (9,9))
    for edge in edges:
        plt.plot(edge[:,0], edge[:, 1], 'k-')

    for face in faces:
        plt.fill(face[:, 0], face[:, 1], 'b', alpha=0.4)

    plt.plot(vertices[:,0], vertices[:,1], 'o')

    plt.title("$\mathrm{VR}_r(V)$ with $r$=" + str(args.delta) + f" with noise $\epsilon\sim U(-{args.epsilon},{args.epsilon})$")
    plt.grid(True)
    plt.savefig(os.path.join(args.path_to_output, f"vr_{args.delta}.pdf"))
    # plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Computes Rips of Circle.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--path_to_output', type=str, help="Path to output directory", required=True)
    parser.add_argument('--num_points', type=int, help="Number of points.", default=100)
    parser.add_argument('--radius', type=float, help="Radius of circle", default=1)
    parser.add_argument('--delta', type=float, help="Delta for Rips.", default=0.3)
    parser.add_argument('--epsilon', type=float, help="Epsilon for noise.", default=0.3)
    args = parser.parse_args()
    main(args)
