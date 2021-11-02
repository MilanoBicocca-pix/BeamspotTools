#!/usr/bin/python

import iminuit
import numpy as np
from scipy.stats import multivariate_normal
from time import time
from MultiVariateGauss import MultivariateGaussianFitterNLL, AltMultivariateGaussianFitterNLL


class PVfitterCMS(AltMultivariateGaussianFitterNLL):
    '''
    '''
    def __init__(self, positions, uncertainties=None, correlations=None, errorscale=1., verbose=False):
        super(PVfitterCMS, self).__init__(positions, uncertainties, correlations, errorscale, verbose)
        self.tilts = np.array([0., 0.]).astype('float64')
        self.corrxy = 0.
        if uncertainties is not None and correlations is not None:
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
            corrxy=self.corrxy,
            dxdz=self.tilts[0],
            dydz=self.tilts[1],
            sigma_x_eff=self.widths[0],
            sigma_y_eff=self.widths[1],
            sigma_z_eff=self.widths[2],
            fix_corrxy=True,      
            fix_dxdz=True,      
            fix_dydz=True,      
            fix_sigma_x_eff=True,      
            fix_sigma_y_eff=True,      
            fix_sigma_z_eff=True,      
        )
        
        try:
            # run the minimization            
            minimizer.migrad()
            
            self.positions[0] = minimizer.values['x']
            self.positions[1] = minimizer.values['y']
            self.positions[2] = minimizer.values['z']
        except:
            print ('ERROR! NLL Minimization failed')
        
        return minimizer

    def fitWidths(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            corrxy=self.corrxy,
            dxdz=self.tilts[0],
            dydz=self.tilts[1],
            sigma_x_eff=self.widths[0],
            sigma_y_eff=self.widths[1],
            sigma_z_eff=self.widths[2],
            fix_x=True,      
            fix_y=True,      
            fix_z=True,      
            fix_corrxy=True,      
            fix_dxdz=True,      
            fix_dydz=True,      
        )

        try:       
            # run the minimization            
            minimizer.migrad()
            
            self.widths[0] = minimizer.values['sigma_x_eff']
            self.widths[1] = minimizer.values['sigma_y_eff']
            self.widths[2] = minimizer.values['sigma_z_eff']
        except:
            print ('ERROR! NLL Minimization failed')
        
        return minimizer

    def fitAllButTilts(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            corrxy=self.corrxy,
            dxdz=self.tilts[0],
            dydz=self.tilts[1],
            sigma_x_eff=self.widths[0],
            sigma_y_eff=self.widths[1],
            sigma_z_eff=self.widths[2],
            fix_corrxy=True,      
            fix_dxdz=True,      
            fix_dydz=True,      
        )
        
        try:
            # run the minimization            
            minimizer.migrad()
            self.positions[0] = minimizer.values['x']
            self.positions[1] = minimizer.values['y']
            self.positions[2] = minimizer.values['z']
            self.widths[0] = minimizer.values['sigma_x_eff']
            self.widths[1] = minimizer.values['sigma_y_eff']
            self.widths[2] = minimizer.values['sigma_z_eff']
        except:
            print ('ERROR! NLL Minimization failed')
        
        return minimizer    
    
    def fitCorrXY(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            corrxy=self.corrxy,
            dxdz=self.tilts[0],
            dydz=self.tilts[1],
            sigma_x_eff=self.widths[0],
            sigma_y_eff=self.widths[1],
            sigma_z_eff=self.widths[2],
            fix_x=True,      
            fix_y=True,      
            fix_z=True,      
            limit_corrxy=(-1., 1.),
            fix_dxdz=True,
            fix_dydz=True,
            fix_sigma_x_eff=True,      
            fix_sigma_y_eff=True,      
            fix_sigma_z_eff=True,      
        )
        
        try:
            # run the minimization            
            minimizer.migrad()
            self.corrxy = minimizer.values['corrxy']
        except:
            print ('ERROR! NLL Minimization failed')
        
        return minimizer
    
    def fitTilts(self):
        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            corrxy=self.corrxy,
            dxdz=self.tilts[0],
            dydz=self.tilts[1],
            sigma_x_eff=self.widths[0],
            sigma_y_eff=self.widths[1],
            sigma_z_eff=self.widths[2],
            fix_x=True,      
            fix_y=True,      
            fix_z=True,      
            fix_corrxy=True,
            limit_dxdz=(-0.0004, 0.0004),
            limit_dydz=(-0.0004, 0.0004),
            fix_sigma_x_eff=True,      
            fix_sigma_y_eff=True,      
            fix_sigma_z_eff=True,      
        )
        
        try:
            # run the minimization            
            minimizer.migrad()
            self.tilts[1] = minimizer.values['dxdz']
            self.tilts[2] = minimizer.values['dydz']        
        except:
            print ('ERROR! NLL Minimization failed')
        
        return minimizer
    
    def fit(self):
        #self.fitPositions()
        #self.fitWidths()
        self.fitAllButTilts()
        self.fitCorrXY()
        self.fitTilts()

        minimizer = iminuit.Minuit(
            self.fcn,
            pedantic=False,
            x=self.positions[0],
            y=self.positions[1],
            z=self.positions[2],
            corrxy=self.corrxy,
            dxdz=self.tilts[0],
            dydz=self.tilts[1],
            sigma_x_eff=self.widths[0],
            sigma_y_eff=self.widths[1],
            sigma_z_eff=self.widths[2],
            limit_corrxy=(-1., 1.),
            limit_dxdz=(-0.0004, 0.0004),
            limit_dydz=(-0.0004, 0.0004),
            limit_sigma_x_eff=(0.,100.),
            limit_sigma_y_eff=(0.,100.),
            limit_sigma_z_eff=(0.,100.),
            print_level=self.verbose,
        ) 
        
        try:       
            # run the minimization            
            minimizer.migrad() 
            self.positions[0] = minimizer.values['x']
            self.positions[1] = minimizer.values['y']
            self.positions[2] = minimizer.values['z']
            self.widths[0] = minimizer.values['sigma_x_eff']
            self.widths[1] = minimizer.values['sigma_y_eff']
            self.widths[2] = minimizer.values['sigma_z_eff']
            self.corrxy = minimizer.values['corrxy']
            self.tilts[1] = minimizer.values['dxdz']
            self.tilts[2] = minimizer.values['dydz']        
       
        except:
            print ('ERROR! NLL Minimization failed')
        
        return minimizer








if __name__ == '__main__':

    # ---------- GENERATE EVENTS -----------
    # generate events with somewhat realistic parameters
    ntoys = 10000
          
    # centroid       position
    pos = np.array([0.066, 0.094, 0.5,])
#     pos = np.array([0., 0., 0.,])
#     pos = np.array([1., 2., 5.,])
#     pos = np.array([1., 2., 25.,])
    
    # build the covariance matrix from angles and widths
    cov = MultivariateGaussianFitterNLL._compute_covariance_matrix(
        theta_x= 0.00015, #[rad]
        theta_y= 0., #[rad]
        theta_z= 0., #[rad]
        sigma_x= 0.0008, #[cm]
        sigma_y= 0.0007, #[cm]
        sigma_z= 3.5, #[cm]
    )
    
    # fix random seed
    rng = np.random.RandomState(1986)
    
    # generate multivariate normal
    mvg = rng.multivariate_normal(pos, cov, ntoys)
    
    print ('generated %d toys' %ntoys)
    
    # create PVfitter object
    beamspot = PVfitterCMS(mvg, verbose=False)
    
    # initialise tilts...
#     beamspot.corrxy = 0.1
#     beamspot.tilts = np.array([0.00015, 0.])

    
    # fit
    results = beamspot.fit()
    
    status = results.get_fmin()
    print ('\n========== FIT VALIDITY ============')
    print ('for info http://iminuit.readthedocs.io/en/latest/api.html#return-value-struct')
    for k, v in vars(status).iteritems(): print (k, v)
    
    # print results
    print ('\n========== FIT RESULTS ============')
    for k in ['x', 'y', 'z', 'corrxy', 'dxdz', 'dydz', 
              'sigma_x_eff', 'sigma_y_eff', 'sigma_z_eff']:
        print ('%s:\t %.10f +/- %.12f [cm]' %(k, results.values[k], results.errors[k]))
    
