#
# persistence_diagrams.py
# -----------------------
#

#
# visualize.py
# ------------
# Visualizes Ising data files
# as tori.
#

import json
import os, sys
import argparse

import numpy as np
import dionysus as d
import matplotlib.pyplot as plt

from map_torus import map_image_to_torus

def generate_barcode(persistence, filtration, dimension):
    barcode = []
    num_persistent = 0
    for i in range(len(persistence)):
        if persistence.pair(i) < i: continue
        dim = filtration[i].dimension()
        if dim != dimension: continue
        if persistence.pair(i) != persistence.unpaired:
            barcode += [{'b': i, 'd': persistence.pair(i)}]
        else:
            barcode += [{'b': i}]
            num_persistent += 1
    return barcode, num_persistent

def plot_rips(ax, f, points, length):
    vertices = []
    edges = []
    faces = []
    for simplex in f:
        try:
            if simplex.dimension() == 0:
                vertices.append(points[simplex[0]])
            elif simplex.dimension() == 1:
                edges.append([points[simplex[0]], points[simplex[1]]])
            elif simplex.dimension() == 2:
                faces.append([points[simplex[0]], points[simplex[1]], points[simplex[2]]])
        except:
            continue

    vertices = np.asarray(vertices)
    edges = np.asarray(edges)
    faces = np.asarray(faces)

    if vertices.shape[0] == 0:
        return
    if edges.shape[0] == 0:
        return

    ax.scatter3D(points[:, 0], points[:, 1], points[:, 2], c='r', s=0.4)
    for edge in edges:
        ax.plot(edge[:, 0], edge[:,1], edge[:,2], 'k-', alpha=0.2, linewidth=0.4)
    ax.set_xlim([-length, length])
    ax.set_ylim([-length, length])
    ax.set_zlim([-length, length])

def plot_barcode(ax, barcode, persistence):
    num_lines = len(barcode)
    num_pts = len(persistence)

    for i in range(num_lines):
        b_id = barcode[i]['b']
        d_id =  barcode[i]['d'] if 'd' in barcode[i] else num_pts

        domain = np.arange(b_id, d_id, 1)
        ax.plot(domain, i*np.ones(domain.shape)/10.0, ('b' if (d_id - b_id) / num_pts > 0.2 else 'k') if 'd' in barcode[i] else 'r', linewidth=0.8)


def main(args):
    args_file = open(os.path.join(args.path_to_folder, "args.json"), 'r')
    data = json.load(args_file)
    args_file.close()

    num_measurements = data["num_measurements"]
    T = np.linspace(data["min_T"], data["max_T"], num_measurements)

    print(f"Computing {num_measurements} persistence diagrams...")
    for i in range(num_measurements):
        img = np.load(os.path.join(args.path_to_folder, f"{i}.npy"))

        a = args.a
        b = args.b
        # Choose more dominant magnetization batches to compute homology
        torus = map_image_to_torus(img == (-1 if np.mean(img) < 0 else 1), a, b)

        f = d.fill_rips(torus, 2, 0.9)
        m = d.homology_persistence(f)
        barcode, num_persistent = generate_barcode(m, f, args.dim)

        fig = plt.figure(figsize=(9,9))
        ax = fig.add_subplot(111, projection='3d')
        plot_rips(ax, f, torus, 2*b)
        plt.savefig(os.path.join(args.path_to_output, f"{i}_torus.svg"), format='svg')

        fig_barcode = plt.figure(figsize = (17,9))
        ax_barcode = fig_barcode.add_subplot(111)
        plot_barcode(ax_barcode, barcode, m)
        ax_barcode.set_xlabel("Filtration")
        ax_barcode.set_ylabel("Generator")
        ax_barcode.grid(True)
        ax_barcode.set_title(f"Persistence barcode of $H_{args.dim}(R_\delta)$ at $T={T[i]}$. Persistent generators {num_persistent}.")
        plt.savefig(os.path.join(args.path_to_output, f"{i}_barcode.svg"), format='svg')

        # Progress
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%% at T=%.02f" % ('='*int(20 * (i+1) / num_measurements), 100*(i+1) / num_measurements, T[i]))
        sys.stdout.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Computes Persistence of torus.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--path_to_folder', type=str, help="Path to the folder containing ising simulation data.", required=True)
    parser.add_argument('--path_to_output', type=str, help="Path to the output folder", required=True)
    parser.add_argument('--dim', type=int, help="Dimension of homology. 0 or 1.", default=1)
    parser.add_argument('--a', type=float, help="Torus inner.", default = 1)
    parser.add_argument('--b', type=float, help="Torus outer.", default = 2)
    args = parser.parse_args()
    main(args)
