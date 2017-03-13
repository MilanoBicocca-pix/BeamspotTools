#!/usr/bin/python

import iminuit
import numpy as np
from scipy.stats import multivariate_normal
from time import time
from MultiVariateGauss import MultivariateGaussianFitterNLL


class PVfitter(MultivariateGaussianFitterNLL):
    '''
    '''
    def __init__(self, positions, uncertainties=None, verbose=False):
        self.events = positions
        self.uncertainties = uncertainties
        self.positions = np.mean(positions, axis=0)
        self.widths = np.std(positions, axis=0)
        self.thetas = np.array([0., 0., 0.]).astype('float64')
        self.verbose = verbose
        if uncertainties is not None:
            self.fcn = self.nlle
        else:
            self.fcn = self.nll
        
        
    def fitPositions(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            theta_x=self.thetas[0],
            theta_y=self.thetas[1],
            theta_z=self.thetas[2],
            sigma_x=self.widths[0],
            sigma_y=self.widths[1],
            sigma_z=self.widths[2],
            fix_theta_x=True,      
            fix_theta_y=True,      
            fix_theta_z=True,      
            fix_sigma_x=True,      
            fix_sigma_y=True,      
            fix_sigma_z=True,      
        )
        
        try:
            # run the minimization            
            minimizer.migrad()
            
            self.positions[0] = minimizer.values['x']
            self.positions[1] = minimizer.values['y']
            self.positions[2] = minimizer.values['z']
        except:
            print 'ERROR! NLL Minimization failed'
        
        return minimizer

    def fitWidths(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            theta_x=self.thetas[0],
            theta_y=self.thetas[1],
            theta_z=self.thetas[2],
            sigma_x=self.widths[0],
            sigma_y=self.widths[1],
            sigma_z=self.widths[2],
            fix_x=True,      
            fix_y=True,      
            fix_z=True,      
            fix_theta_x=True,      
            fix_theta_y=True,      
            fix_theta_z=True,      
        )

        try:       
            # run the minimization            
            minimizer.migrad()
            
            self.widths[0] = minimizer.values['sigma_x']
            self.widths[1] = minimizer.values['sigma_y']
            self.widths[2] = minimizer.values['sigma_z']
        except:
            print 'ERROR! NLL Minimization failed'
        
        return minimizer

    def fitThetas(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            theta_x=self.thetas[0],
            theta_y=self.thetas[1],
            theta_z=self.thetas[2],
            sigma_x=self.widths[0],
            sigma_y=self.widths[1],
            sigma_z=self.widths[2],
            fix_x=True,      
            fix_y=True,      
            fix_z=True,      
            # fix_theta_z=True, # no tilt along the z axis   
            limit_theta_z=(-np.pi/2., np.pi/2.), # resolve periodicity, but leave theta_z free
            fix_sigma_x=True,      
            fix_sigma_y=True,      
            fix_sigma_z=True,      
        )
        
        try:
            # run the minimization            
            minimizer.migrad()
            self.thetas[0] = minimizer.values['theta_x']
            self.thetas[1] = minimizer.values['theta_y']
            self.thetas[2] = minimizer.values['theta_z']        
        except:
            print 'ERROR! NLL Minimization failed'
        
        return minimizer
    
    def fit(self):
        self.fitPositions()
        self.fitWidths()
        self.fitThetas()

        minimizer = iminuit.Minuit(
            self.nll,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            theta_x=self.thetas[0],
            theta_y=self.thetas[1],
            theta_z=self.thetas[2],
            sigma_x=self.widths[0],
            sigma_y=self.widths[1],
            sigma_z=self.widths[2],
            #fix_theta_z=True, # no tilt along the z axis   
            limit_theta_z=(-np.pi/2., np.pi/2.), # resolve periodicity, but leave theta_z free
        ) 
        
        try:       
            # run the minimization            
            minimizer.migrad() 
            self.positions[0] = minimizer.values['x']
            self.positions[1] = minimizer.values['y']
            self.positions[2] = minimizer.values['z']
            self.widths[0] = minimizer.values['sigma_x']
            self.widths[1] = minimizer.values['sigma_y']
            self.widths[2] = minimizer.values['sigma_z']
            self.thetas[0] = minimizer.values['theta_x']
            self.thetas[1] = minimizer.values['theta_y']
            self.thetas[2] = minimizer.values['theta_z']
       
        except:
            print 'ERROR! NLL Minimization failed'
        
        return minimizer








if __name__ == '__main__':

    # ---------- GENERATE EVENTS -----------
    # generate events with somewhat realistic parameters
    ntoys = 200000
          
    # centroid       position
#     pos = np.array([0.066, 0.094, 0.5,])
#     pos = np.array([0., 0., 0.,])
#     pos = np.array([1., 2., 5.,])
    pos = np.array([1., 2., 25.,])
    
    # build the covariance matrix from angles and widths,
    # easier to read
    cov = MultivariateGaussianFitterNLL._compute_covariance_matrix(
#         theta_x= 0.00015, #[rad]
        theta_x= 0.15, #[rad]
        theta_y=-0.00002, #[rad]
        theta_z= 0.2, #[rad]
        sigma_x= 0.0085, #[cm]
        sigma_y= 0.0077, #[cm]
        sigma_z= 3.4 #[cm]
    )
    
    # fix random seed
    rng = np.random.RandomState(1986)
    
    # generate multivariate normal
    mvg = rng.multivariate_normal(pos, cov, ntoys)
    
    print 'generated %d toys' %ntoys
    
    # create PVfitter object
    beamspot = PVfitter(mvg)
    
    # fit
    results = beamspot.fit()
    
    # print results
    print '\n========== FIT RESULTS ============'
    for k in ['x', 'y', 'z', 'theta_x', 'theta_y', 'theta_z', 
              'sigma_x', 'sigma_y', 'sigma_z']:
        print '%s:\t %.5f +/- %.6f [cm]' %(k, results.values[k], results.errors[k])
    
