#!/usr/bin/python

import iminuit
import numpy as np
from scipy.stats import multivariate_normal

# from time import time

class MultivariateGaussianFitterNLL(object):
    '''
    Fit 3D gaussian cloud.
    '''
    def __init__(self, events, uncertainties=None, correlations=None, errorscale=1., verbose=False):
        self.events        = events.astype(np.float64)
        self.uncertainties = uncertainties.astype(np.float64)
        self.correlations  = correlations.astype(np.float64)
        self.errorscale    = errorscale
        self.positions     = np.mean(events, axis=0).astype(np.float64)
        self.widths        = np.std(events, axis=0).astype(np.float64)
        self.verbose       = verbose # should use a logger...
        self.nevents       = len(self.events)/3
        self.rnevents      = np.arange(self.nevents)
      
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
            print 'covariance matrix', cov
            print 'determinant: ', np.linalg.det(cov) 
        
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
        cov_beam = self._compute_covariance_matrix(theta_x,
                                                   theta_y,
                                                   theta_z,
                                                   sigma_x,
                                                   sigma_y,
                                                   sigma_z)
                                                   
        return self._compute_sum_nll_vtx(cov_beam, x, y, z)
                                                   

    def _compute_sum_nll_vtx(self, cov_beam, x, y, z):

        nlls = np.array([]).astype(np.float64)

        for i in self.rnevents:
            vtx_xx = np.power(self.errorscale * self.uncertainties[i][0], 2)
            vtx_yy = np.power(self.errorscale * self.uncertainties[i][1], 2)
            vtx_zz = np.power(self.errorscale * self.uncertainties[i][2], 2)
    
            vtx_xy = self.correlations[i][0] * self.errorscale * self.uncertainties[i][0] * self.errorscale * self.uncertainties[i][1]
            vtx_xz = self.correlations[i][1] * self.errorscale * self.uncertainties[i][0] * self.errorscale * self.uncertainties[i][2]
            vtx_yz = self.correlations[i][2] * self.errorscale * self.uncertainties[i][1] * self.errorscale * self.uncertainties[i][2]
    
            cov_vtx = np.matrix([
                [vtx_xx, vtx_xy, vtx_xz],
                [vtx_xy, vtx_yy, vtx_yz],
                [vtx_xz, vtx_yz, vtx_zz],
            ]).astype(np.float64)

            cov_tot = cov_vtx + cov_beam
            
            nll = -multivariate_normal.logpdf(self.events[i],
                                              mean=np.array([x, y, z]),
                                              cov=cov_tot,
                                              allow_singular=True) # this was needed because?
            
            if self.verbose and i%20==0:
                print '\t====> evaluated %d/%d vertex, nll = %f, sum nll = %f' %(i, self.nevents, nll, nlls.sum())

            nlls = np.append(nlls, nll)
                        
        return nlls.sum()
    



class AltMultivariateGaussianFitterNLL(MultivariateGaussianFitterNLL):
    '''
    '''
    
    @staticmethod
    def _compute_covariance_matrix(corrxy, sigma_x_eff, sigma_y_eff, sigma_z_eff, dxdz, dydz):
        sx  = sigma_x_eff
        sy  = sigma_y_eff
        sz  = sigma_z_eff
        sx2 = np.power(sigma_x_eff, 2)
        sy2 = np.power(sigma_y_eff, 2)
        sz2 = np.power(sigma_z_eff, 2)
        
        cov = np.matrix([
            [sx2                                         , corrxy * sx * sy                            , - dxdz * (sz2-sx2) - dydz * corrxy * sx * sy],
            [corrxy * sx * sy                            , sy2                                         , - dydz * (sy2-sz2) + dxdz * corrxy * sx * sy],
            [- dxdz * (sz2-sx2) - dydz * corrxy * sx * sy, - dydz * (sy2-sz2) + dxdz * corrxy * sx * sy, sz2                                         ],
        ]).astype(np.float64)
        
        return cov    
    
    def nll(self, x, y, z, corrxy, sigma_x_eff, sigma_y_eff, sigma_z_eff, dxdz, dydz):
        '''
        Modeled on official CMS beam spot fit.
        https://github.com/cms-sw/cmssw/blob/master/RecoVertex/BeamSpotProducer/src/FcnBeamSpotFitPV.cc#L59
        '''
        if self.verbose:
            print '\n=========='
            print 'x                :\t', x          , '[cm]'
            print 'y                :\t', y          , '[cm]'
            print 'z                :\t', z          , '[cm]'
            print 'corrxy           :\t', corrxy
            print 'effective sigma x:\t', sigma_x_eff, '[cm]'
            print 'effective sigma y:\t', sigma_y_eff, '[cm]'
            print 'effective sigma z:\t', sigma_z_eff, '[cm]'
            print 'dx/dz            :\t', dxdz
            print 'dy/dz            :\t', dydz
        
        cov = self._compute_covariance_matrix(corrxy, sigma_x_eff, sigma_y_eff, sigma_z_eff, dxdz, dydz)
        
        if self.verbose:
            print 'covariance matrix', cov
            print 'determinant: ', np.linalg.det(cov) 
        
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

    def nlle(self, x, y, z, corrxy, sigma_x_eff, sigma_y_eff, sigma_z_eff, dxdz, dydz):
        '''
        '''
        cov_beam = self._compute_covariance_matrix(corrxy, 
                                                   sigma_x_eff, 
                                                   sigma_y_eff, 
                                                   sigma_z_eff, 
                                                   dxdz, 
                                                   dydz)
        return self._compute_sum_nll_vtx(cov_beam, x, y, z)


if __name__ == '__main__':
    pass
    
    
    
