#
# simulate.py
# -----------
# Runs Ising simulation.
#

import json
import os, sys
import argparse

import numpy as np
import matplotlib.pyplot as plt

from ising import Ising

def main(args):
    T = np.linspace(args.min_T, args.max_T, args.num_measurements)
    # Magnetizations
    mu = []

    print(f"Starting Ising simulation with shape: ({args.size},{args.size}) and for {T.shape[0]} iterations...")
    for i in range(T.shape[0]):
        beta = 1.0/T[i]

        ising = Ising((args.size, args.size))
        magnetization = 0
        for _ in range(args.num_eq_iters):
            ising.monteCarloStep(beta)

        for _ in range(args.num_average_iters):
            ising.monteCarloStep(beta)
            magnetization += ising.calculateMagnetization()

        np.save(os.path.join(args.path_to_output, str(i)), ising.getState)

        # Record magnetization
        mu.append(magnetization / args.num_average_iters)

        # Progressbar
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('='*int(20 * (i+1) / T.shape[0]), 100*(i+1) / T.shape[0]))
        sys.stdout.flush()

    data = {
        'size': args.size,
        'min_T': args.min_T,
        'max_T': args.max_T,
        'num_measurements': args.num_measurements,
        'num_eq_iters': args.num_eq_iters,
        'num_average_iters': args.num_average_iters
    }

    with open(os.path.join(args.path_to_output, "args.json"), 'w') as f:
        json.dump(data, f)

    plt.figure(figsize=(9,9))
    plt.plot(T, np.abs(mu), 'o')
    plt.grid(True)
    plt.xlabel("Temperature $T$")
    plt.ylabel("Magnetization $\\mu$")
    plt.title(f"Magnetization for Ising model of shape ({args.size}, {args.size})")
    plt.savefig(os.path.join(args.path_to_output, "magnetization.eps"))
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs simulation of 2D ising model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--path_to_output', type=str, help="Path to the output directory.")

    parser.add_argument('--size', type=int, help="Specified the size of lattice.", default=32)
    parser.add_argument('--num_measurements',
        type=int, help="Specifies the number of measurements to make after model reaches equilibrium (if exists).", default=32)
    parser.add_argument('--min_T', type=float, help="Specifies minimum temperature.", default = 1.1)
    parser.add_argument('--max_T', type=float, help="Specifies the maximum temperature.", default = 3.0)

    parser.add_argument('--num_eq_iters',
        type=int, help="Specifies the number of iterations for reaching equilibrium (if exists).", default=2**8)
    parser.add_argument('--num_average_iters',
        type=int, help="Specifies the number of iterations for averaging.", default=2**9)

    args = parser.parse_args()
    main(args)
