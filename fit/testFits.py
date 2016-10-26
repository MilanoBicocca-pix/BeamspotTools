import ROOT
import numpy as np
import matplotlib.pyplot as plt

ntoys = 4000

pars = np.array([0.057419, 0.10088, 0.570405])

cov1 = np.array([[ 5.66734e-09, -4.78987e-11, 0         ],
                 [-4.78987e-11,  5.74355e-09, 0         ],
                 [ 0          ,  0          , 0.00559112]])

cov2 = np.array([[ 1.00622e-08,  0          , 0         ],
                 [ 0          ,  1.00622e-08, 0         ],
                 [ 0          ,  0          , 0.00279565]])

cov = cov1 + cov2

# fix random seed
rng = np.random.RandomState(1986)

# generate multivariate normal
mvg = rng.multivariate_normal(pars, cov, ntoys)



plt.scatter(mvg[:,0], mvg[:,1], c='r')


# from scipy.stats import multivariate_normal
# 
# x, y = np.mgrid[-1.0:1.0:30j, -1.0:1.0:30j]
# # Need an (N, 2) array of (x, y) pairs.
# xy = np.column_stack([x.flat, y.flat])
# 
# mu = np.array([0.0, 0.0])
# 
# sigma = np.array([.025, .025])
# covariance = np.diag(sigma**2)
# 
# z = multivariate_normal.pdf(xy, mean=mu, cov=covariance)
# 
# # Reshape back to a (30, 30) grid.
# z = z.reshape(x.shape)