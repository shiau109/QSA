import numpy as np
from sklearn.mixture import GaussianMixture

from sklearn.datasets import make_blobs

import matplotlib.pyplot as plt
sim_data, sim_data_label = make_blobs(n_samples=400, centers=3,
                       cluster_std=0.60, random_state=0)

# X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

plt.scatter(sim_data[:, 0], sim_data[:, 1], s=40, cmap='viridis')
# print(gm.means_)
gm = GaussianMixture(n_components=2, random_state=0).fit(sim_data)

# print(gm.means_)

print(gm.predict([[0, 0], [12, 3]]))
plt.show()