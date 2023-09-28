import numpy as np
from sklearn.mixture import GaussianMixture

from sklearn.datasets import make_blobs

import matplotlib.pyplot as plt
sim_data, sim_data_label = make_blobs(n_samples=400, centers=3,
                       cluster_std=0.60, random_state=0)

# data = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

# print(gm.means_)
# gm = GaussianMixture(n_components=2, random_state=0).fit(sim_data)

# print(gm.means_)

# print(gm.predict([[0, 0], [12, 3]]))
# plt.show()



from matplotlib.patches import Ellipse

def draw_ellipse(position, covariance, ax=None, **kwargs):
    ax = ax or plt.gca()
    
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    
    # Draw the Ellipse
    for nsig in range(1, 4):
        ax.add_patch(Ellipse(position, nsig * width, nsig * height,
                             angle, **kwargs))
        
def plot_gmm(gmm, data, label=True, ax=None):
    ax = ax or plt.gca()
    labels = gmm.fit(data).predict(data)
    if label:
        ax.scatter(data[:, 0], data[:, 1], c=labels, s=40, cmap='viridis', zorder=2)
    else:
        ax.scatter(data[:, 0], data[:, 1], s=40, zorder=2)
    ax.axis('equal')
    
    w_factor = 0.2 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covars_, gmm.weights_):
        draw_ellipse(pos, covar, alpha=w * w_factor)
        
        
gmm = GMM(n_components=3, random_state=0)
plot_gmm(gmm, data)