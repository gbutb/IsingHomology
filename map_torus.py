#
# map_torus.py
# ------------
# Contains code for mapping an (n,m) square
# with identified edges to a torus.
#


import numpy as np


def map_image_to_torus(mask, a, b):
    """
    Takes image and maps the valid/masked points to torus.

    Parameters
    ----------
    mask: np.ndarray
        Shape: (n,m) binary/bool array.

    a: float
        inner radius of torus.

    b: float
        outer radius of torus.

    Returns
    -------
    points: np.ndarray
        Shape: (N, 3), where N is the number of points s.t. mask = True
    """
    points = []
    theta = np.linspace(0, 2*np.pi, mask.shape[0])
    phi = np.linspace(0, 2*np.pi, mask.shape[1])
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if not mask[i, j]:
                continue

            x = (b + a * np.cos(theta[i])) * np.cos(phi[j])
            y = (b + a * np.cos(theta[i])) * np.sin(phi[j])
            z = a * np.sin(theta[i])

            points.append([x,y,z])

    return np.asarray(points)
