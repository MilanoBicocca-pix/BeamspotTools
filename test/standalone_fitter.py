import sys
sys.path.append('..')

from objects.PVfitter import PVfitter
from objects.BeamSpot import BeamSpot
from objects.Payload  import Payload

import root_numpy as rn
import numpy as np


myarray = rn.root2array(
#             '/afs/cern.ch/user/f/fiorendi/public/BeamFit_LumiBased_Workflow_onJetHT_alcareco.root',
            '~/Desktop/beamspotter/BeamFit_LumiBased_Workflow_onJetHT_alcareco.root',
            'PrimaryVertices;4',
          )

ls = list(set(myarray['lumi']))


allbs = []


for ils in ls:

    print ('running on LS %d' %ils)
    
    # find entries with a given lumi
    mask = myarray['lumi']==ils
    
    # slice down the positons of these entries
    positions = myarray[mask]['pvData_position']
        
    # print '\tsliced'
    beamspot = PVfitter(positions)
    results = beamspot.fit()
    
    # print '\tfitted'
    bs = BeamSpot()
    
    bs.Type          =  2 * results.migrad_ok()
    bs.X             =  results.values['x']
    bs.Xerr          =  results.errors['x']
    bs.Y             =  results.values['y']
    bs.Yerr          =  results.errors['y']
    bs.Z             =  results.values['z']
    bs.Zerr          =  results.errors['z']
    bs.sigmaZ        =  results.values['sigma_z']
    bs.sigmaZerr     =  results.errors['sigma_z']
    bs.dxdz          =  results.values['theta_y']
    bs.dxdzerr       =  results.errors['theta_y']
    bs.dydz          =  results.values['theta_x']
    bs.dydzerr       =  results.errors['theta_x']
    bs.beamWidthX    =  results.values['sigma_x']
    bs.beamWidthXerr =  results.errors['sigma_x']
    bs.beamWidthY    =  results.values['sigma_y']
    bs.beamWidthYerr =  results.errors['sigma_y']
    bs.EmittanceX    =  0.
    bs.EmittanceY    =  0.
    bs.betastar      =  0.
    bs.IOVfirst      =  ils
    bs.IOVlast       =  ils
    bs.IOVBeginTime  =  0.
    bs.IOVEndTime    =  0.
    bs.Run           =  283416
    bs.XYerr         =  0.
    bs.YXerr         =  0.
    bs.dxdzdydzerr   =  0.
    bs.dydzdxdzerr   =  0.
    
    allbs.append(bs)
    
    bs.Dump('payload_run283416.txt')
    

payload = Payload('payload_run283416.txt')
payload.plot('X', 0, 99999999)    
    
    
