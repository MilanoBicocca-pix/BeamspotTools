import numpy as np
from numba import jit, vectorize

def _compute_covariance_matrix_with_arrays(theta_x, theta_y, theta_z, sigma_x, sigma_y, sigma_z):
    '''
    https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Density_function
    '''

    rot_x = np.array([
        [ 1., 0.             ,  0.             ],
        [ 0., np.cos(theta_x), -np.sin(theta_x)],
        [ 0., np.sin(theta_x),  np.cos(theta_x)],
    ]).astype(np.float64)
    
    rot_y = np.array([
        [  np.cos(theta_y), 0., np.sin(theta_y)],
        [  0.             , 1., 0.             ],
        [ -np.sin(theta_y), 0., np.cos(theta_y)],
    ]).astype(np.float64)

    rot_z = np.array([
        [ np.cos(theta_z), -np.sin(theta_z), 0.],
        [ np.sin(theta_z),  np.cos(theta_z), 0.],
        [ 0.             ,  0.             , 1.],
    ]).astype(np.float64)
    
    widths = np.array([
        [ np.power(sigma_x, 2), 0.                  , 0.                  ],
        [ 0.                  , np.power(sigma_y, 2), 0.                  ],
        [ 0.                  , 0.                  , np.power(sigma_z, 2)],
    ]).astype(np.float64)
    
    cov = np.dot(rot_z, widths )
    cov = np.dot(cov  , rot_z.T)
    cov = np.dot(rot_y, cov    )
    cov = np.dot(cov  , rot_y.T)
    cov = np.dot(rot_x, cov    )
    cov = np.dot(cov  , rot_x.T)
        
    return cov



def _compute_covariance_matrix(theta_x, theta_y, theta_z, sigma_x, sigma_y, sigma_z):
    '''
    https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Density_function
    '''

    rot_x = np.matrix([
        [ 1., 0.             ,  0.             ],
        [ 0., np.cos(theta_x), -np.sin(theta_x)],
        [ 0., np.sin(theta_x),  np.cos(theta_x)],
    ]).astype(np.float64)
    
    rot_y = np.matrix([
        [  np.cos(theta_y), 0., np.sin(theta_y)],
        [  0.             , 1., 0.             ],
        [ -np.sin(theta_y), 0., np.cos(theta_y)],
    ]).astype(np.float64)

    rot_z = np.matrix([
        [ np.cos(theta_z), -np.sin(theta_z), 0.],
        [ np.sin(theta_z),  np.cos(theta_z), 0.],
        [ 0.             ,  0.             , 1.],
    ]).astype(np.float64)
    
    widths = np.matrix([
        [ np.power(sigma_x, 2), 0.                  , 0.                  ],
        [ 0.                  , np.power(sigma_y, 2), 0.                  ],
        [ 0.                  , 0.                  , np.power(sigma_z, 2)],
    ]).astype(np.float64)
    
    cov = (rot_x * (rot_y * (rot_z * widths * rot_z.T) * rot_y.T) * rot_x.T)
    
    return cov


@jit(nopython=True)
def _compute_covariance_matrix_numba(theta_x, theta_y, theta_z, sigma_x, sigma_y, sigma_z):
    '''
    https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Density_function
    '''

    rot_x = np.array([
         1., 0.             ,  0.             ,
         0., np.cos(theta_x), -np.sin(theta_x),
         0., np.sin(theta_x),  np.cos(theta_x),
    ]).astype(np.float64).reshape(3,3)
    
    rot_y = np.array([
         np.cos(theta_y), 0., np.sin(theta_y),
         0.             , 1., 0.             ,
        -np.sin(theta_y), 0., np.cos(theta_y),
    ]).astype(np.float64).reshape(3,3)

    rot_z = np.array([
         np.cos(theta_z), -np.sin(theta_z), 0.,
         np.sin(theta_z),  np.cos(theta_z), 0.,
         0.             ,  0.             , 1.,
    ]).astype(np.float64).reshape(3,3)
    
    widths = np.array([
         np.power(sigma_x, 2), 0.                  , 0.                  ,
         0.                  , np.power(sigma_y, 2), 0.                  ,
         0.                  , 0.                  , np.power(sigma_z, 2),
    ]).astype(np.float64).reshape(3,3)
    
    # The following is equivalent to 
    # cov = (rot_x * (rot_y * (rot_z * widths * rot_z.T) * rot_y.T) * rot_x.T)
    # but expressed in a numba-understandable way, to avoid numba falling back to
    # pythonobject mode
    
    cov = np.dot(rot_z, widths )
    cov = np.dot(cov  , rot_z.T)
    cov = np.dot(rot_y, cov    )
    cov = np.dot(cov  , rot_y.T)
    cov = np.dot(rot_x, cov    )
    cov = np.dot(cov  , rot_x.T)
        
    return cov
