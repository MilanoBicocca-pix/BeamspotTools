import ROOT
import numpy as np
from scipy.stats import multivariate_normal


def vertexCloud(x, par):
    x      = x[0]
    y      = x[1]
    z      = x[2]
    parameters = np.array([
        par[0], # x
        par[1], # y
        par[2], # z
        par[3], # sigma x
        par[4], # sigma y
        par[5], # sigma z
    ])
    covariance = np.array([
        [ par[6]*par[6] , -4.78987e-11  , 0.           , 0.           , 0.             , 0.             ],
        [-4.78987e-11   ,  par[7]*par[7], 0.           , 0.           , 0.             , 0.             ],
        [ 0.            ,  0.           , par[8]*par[8], 0.           , 0.             , 0.             ],
        [ 0.            ,  0.           , 0.           , par[9]*par[9], 0.             , 0.             ],
        [ 0.            ,  0.           , 0.           , 0.           , par[10]*par[10], 0.             ],
        [ 0.            ,  0.           , 0.           , 0.           , 0.             , par[11]*par[11]],
    ])

    mvn = multivariate_normal(parameters, covariance)
#     mvn.pd