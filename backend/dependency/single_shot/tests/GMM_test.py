import numpy as np
from sklearn.mixture import GaussianMixture

# from sklearn.mixture import GMM

from sklearn.datasets import make_blobs
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

sim_point = 10000
signal_dis = 5
noise = 1

train_ratio_0 = 0.4
train_point_0 = int(sim_point*train_ratio_0)
train_point_1 = sim_point-train_point_0
training_mu_I0 = 0
training_mu_Q0 = 0
training_sig_0 = [np.random.normal(training_mu_I0, noise, train_point_0), np.random.normal(training_mu_Q0, noise, train_point_0)]

training_mu_I1 = training_mu_I0+signal_dis
training_mu_Q1 = 0
training_sig_1 = [np.random.normal(training_mu_I1, noise, train_point_1), np.random.normal(training_mu_Q1, noise, train_point_1)]

training_data_I = np.append(training_sig_0[0],training_sig_1[0])
training_data_Q = np.append(training_sig_0[1],training_sig_1[1])
training_data = np.array([training_data_I,training_data_Q]).transpose()

pop_0 = 0.9
point_0 = int(sim_point*pop_0)
point_1 = sim_point -point_0 

data_mu_I0 = training_mu_I0
data_mu_Q0 = training_mu_Q0
data_mu_I1 = training_mu_I1
data_mu_Q1 = training_mu_Q1
sim_data_I = np.append(np.random.normal(data_mu_I0, noise, point_0), np.random.normal(data_mu_I1, noise, point_1))
sim_data_Q = np.append(np.random.normal(data_mu_Q0, noise, point_0), np.random.normal(data_mu_Q1, noise, point_1))
sim_data = np.array([sim_data_I,sim_data_Q]).transpose()

# sim_data, sim_data_label = make_blobs(n_samples=400, centers=3,
#                        cluster_std=0.60, random_state=0)



# data = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

# print(gm.means_)
# print(gm.predict([[0, 0], [12, 3]]))
# plt.show()



from matplotlib.patches import Ellipse



def draw_ellipse(position, covariance, ax=None, **kwargs):

    # print("kwargs type",type(kwargs))

    ax = ax or plt.gca()
    
    # Convert covariance to principal axes
    if covariance.shape == (2, 2):
        U, s, Vt = np.linalg.svd(covariance)
        angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
        width, height = 2 * np.sqrt(s)
    else:
        angle = 0
        width, height = 2 * np.sqrt(covariance)
    kwargs["angle"] = angle
    # Draw the Ellipse
    for nsig in range(1, 4):
        print(position, nsig*width, nsig*height,angle)
        ax.add_patch( Ellipse(position, nsig*width, nsig*height, angle=angle, **kwargs ))
        
from matplotlib import transforms

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    ax = ax or plt.gca()
    print(kwargs)
    # ax = plt.gca()
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    ax.add_patch(ellipse)
    # return 

def plot_gmm(gmm:GaussianMixture, data, label=True, ax=None):
    ax = ax or plt.gca()
    labels = gmm.predict(data)
    # print(labels)
    print(np.bincount(labels))
    print(f'weights {gmm.weights_}')

    shot_num = data.shape[0]
    marker_size = 50000/shot_num
    cmap = ListedColormap(["r", "b"])
    if label:
        ax.scatter(data[:, 0], data[:, 1], c=labels, s=marker_size, cmap=cmap, zorder=2, alpha=0.2, linewidths=0 )
    else:
        ax.scatter(data[:, 0], data[:, 1], s=40, zorder=2)
    ax.axis('equal')
    
    w_factor = 0.1 / gmm.weights_.max()
    for pos, covar, w in zip(gmm.means_, gmm.covariances_, gmm.weights_):
        # print(f"mean: {pos}")
        # print(f"covar: {covar}")
        # print(f"weight: {w}")

        draw_ellipse(pos, covar, ax, fc='grey', alpha=w * w_factor)#, alpha=w * w_factor)
    # confidence_ellipse(data[:, 0], data[:, 1], ax, fc='#ACACCA')
        
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_title("Training")
ax2.set_title("Data")

gmm = GaussianMixture(n_components=2, random_state=0)
print(f'Training')

gmm.fit(training_data)

trained = gmm.get_params()
# print(trained)
# print(f'weights{gmm.weights_}')
# print(f'means{gmm.means_}')
# print(f'covariances{gmm.covariances_}')
# print(f'precisions_cholesk{gmm.precisions_cholesky_}')
plot_gmm(gmm, training_data, ax = ax1)
# print(f'cal precisions_cholesk{np.linalg.cholesky(np.linalg.inv(gmm.covariances_))}' ) 

print(f'Predict')

print(sim_data.shape)
new_gmm = GaussianMixture(n_components=2)
new_gmm.precisions_cholesky_ = gmm.precisions_cholesky_
new_gmm.weights_ = gmm.weights_
new_gmm.means_ = gmm.means_
new_gmm.covariances_ = gmm.covariances_
# new_gmm.set_params(trained)
print(sim_data.shape)

# print(sim_data.shape)
plot_gmm(new_gmm, sim_data, ax = ax2)

plt.show()