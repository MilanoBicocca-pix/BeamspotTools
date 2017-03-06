#!/usr/bin/python

import iminuit
import numpy as np
from scipy.stats import multivariate_normal

# from time import time

class MultivariateGaussianFitterNLL():
    '''
    Fit 3D gaussian cloud.
    '''
    def __init__(self, events, uncertainties=None, verbose=False):
        self.events        = events
        self.uncertainties = uncertainties
        self.verbose       = verbose # should use a logger...
        self.nevents       = len(self.events)/3
        self.rnevents      = np.arange(nevents)
      
    @staticmethod
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
                
    def nll(self, x, y, z, theta_x, theta_y, theta_z, sigma_x, sigma_y, sigma_z):
        '''
        '''
        
        if self.verbose:
            print '\n=========='
            print 'x      :\t', x      , '[cm]'
            print 'y      :\t', y      , '[cm]'
            print 'z      :\t', z      , '[cm]'
            print 'theta_x:\t', theta_x, '[rad]'
            print 'theta_y:\t', theta_y, '[rad]'
            print 'theta_z:\t', theta_z, '[rad]'
            print 'sigma x:\t', sigma_x, '[cm]'
            print 'sigma y:\t', sigma_y, '[cm]'
            print 'sigma z:\t', sigma_z, '[cm]'

        cov = self._compute_covariance_matrix(theta_x, theta_y, theta_z, sigma_x, sigma_y, sigma_z)
        
        if self.verbose:
            print 'covariance matrix', np.matrix(cov)
            print 'determinant: ', cov.det()
        
        # check singularity / inveritbility
        if np.linalg.det(cov) > 0.:
            nll = -multivariate_normal.logpdf(self.events,
                                              mean=np.array([x, y, z]),
                                              cov=cov).sum()
        else:
            print 'WARNING! Singular covariance matrix, cannot invert!'
            return float('nan')

        if self.verbose:
            print 'nLL: ', nll
        
        return nll
    
    def nlle(self, x, y, z, theta_x, theta_y, theta_z, sigma_x, sigma_y, sigma_z):
        '''
        '''
        
        #import pdb ; pdb.set_trace()
                        
        nlls = np.array([-multivariate_normal.logpdf(self.events[i],
                                                     mean=np.array([x, y, z]),
                                                     cov=self._compute_covariance_matrix(theta_x,
                                                                                         theta_y,
                                                                                         theta_z, 
                                                                                         sigma_x + self.uncertainties[i][0],
                                                                                         sigma_y + self.uncertainties[i][1],
                                                                                         sigma_z + self.uncertainties[i][2]),
                                                     allow_singular=True) for i in rnevents]).sum()
        
        return nlls


if __name__ == '__main__':
    pass
    
    
    









