from objects.PVfitterCMS import PVfitterCMS
from objects.BeamSpot    import BeamSpot
from objects.Payload     import Payload

from itertools import product
import root_numpy as rn
import numpy as np
import pickle



def groupLS(LSs, maxLS=5, maxGap=1):
    '''
    Groups LS in subgroups of at most maxLS elements.
    maxGap = 1 means consecutive LS. If you allow to have non-concecutive 
    LS in the same group, then increase.
    '''
    nls = len(LSs)
    ils = 1
    allgroups = []
    igroup = []
    
    for i in range(ils, nls):
        if LSs[i]-LSs[i-1] <= maxGap and len(igroup) < maxLS:
            igroup.append(LSs[i-1])
        else:
            ils = i
            allgroups.append(igroup)
            igroup = [LSs[ils]]    
    
    if allgroups[-1] != igroup:
        allgroups.append(igroup)
    
    return allgroups

myarray = rn.root2array(
            '~/Downloads/BeamFit_LumiBased_Workflow_Run283387.root',
            'PrimaryVertices;1',
          )


bxs = sorted(list(set(myarray['bunchCrossing'])))
lss = sorted(list(set(myarray['lumi'])))
lsgroups = groupLS(lss, 6, 2) # group by ls

allbs = []



for igls, ibx in product(lsgroups, bxs):

    print 'running on LSs', igls, 'and BX', ibx
    
    # find entries with a given lumi (not very pythonic, sorry...)
    mask = myarray['lumi']==igls[0]
    for ils in igls[1:]:
        masky = myarray['lumi']==ils
        mask = mask | masky
        print 'ils', ils, 'any(mask==True)', any(mask==True), 'passing entries = ', len(mask[np.where(mask)])
    masky = myarray['bunchCrossing']==ibx
    mask = mask & masky
    print 'ibx', ibx, 'any(mask==True)', any(mask==True), 'passing entries = ', len(mask[np.where(mask)])
        
    # slice down the positons of these entries
    positions = myarray[mask]['pvData_position']

    # slice down the uncertainties of these entries
    uncertainties = myarray[mask]['pvData_posError']

    # slice down the correlations of these entries
    correlations = myarray[mask]['pvData_posCorr']
        
    # print '\tsliced'
    beamspot = PVfitterCMS(positions, uncertainties, correlations, errorscale=0.9, verbose=False)    
    results = beamspot.fit()
    
    # print '\tfitted'
    bs = BeamSpot()
    
    bs.bx            = ibx
    bs.Type          = 2 * results.migrad_ok()
    bs.X             = results.values['x']
    bs.Xerr          = results.errors['x']
    bs.Y             = results.values['y']
    bs.Yerr          = results.errors['y']
    bs.Z             = results.values['z']
    bs.Zerr          = results.errors['z']
    bs.sigmaZ        = results.values['sigma_z_eff']
    bs.sigmaZerr     = results.errors['sigma_z_eff']
    bs.dxdz          = results.values['dxdz']
    bs.dxdzerr       = results.errors['dxdz']
    bs.dydz          = results.values['dydz']
    bs.dydzerr       = results.errors['dydz']
    bs.beamWidthX    = results.values['sigma_x_eff']
    bs.beamWidthXerr = results.errors['sigma_x_eff']
    bs.beamWidthY    = results.values['sigma_y_eff']
    bs.beamWidthYerr = results.errors['sigma_y_eff']
    bs.EmittanceX    = 0.
    bs.EmittanceY    = 0.
    bs.betastar      = 0.
    bs.IOVfirst      = igls[0]
    bs.IOVlast       = igls[-1]
    bs.IOVBeginTime  = 1508250485.0 + 23.3 * (igls[0]  - 100.)
    bs.IOVEndTime    = 1508250485.0 + 23.3 * (igls[-1] - 100.)
    bs.Run           = 283358
    bs.XYerr         = results.values['corrxy'] * results.values['x'] * results.values['y']
    bs.YXerr         = results.values['corrxy'] * results.values['x'] * results.values['y']
    bs.dxdzdydzerr   = 0.
    bs.dydzdxdzerr   = 0.
    bs.corrxy        = results.values['corrxy']
    bs.corrxyerr     = results.errors['corrxy']
    
    bs._computeProperWidths()
    
    allbs.append(bs)
    
    bs.Dump('payload_run283387_errorscale0p9_4LS.txt')
 
# serialise allbs
outfile = open('payload_run283387_errorscale0p9_4LS.pkl', 'w+')
pickle.dump(allbs, outfile)
outfile.close()

# save a txt payload too   
payload = Payload('payload_run283387_errorscale0p9_4LS.txt')
# for var in ['X','Y','Z','beamWidthX','beamWidthY','sigmaXtrue',
#             'sigmaYtrue','sigmaZ','dxdz','dydz','corrxy']:
#     payload.plot(var, 0, 99999999, savePdf=True)    
 
    
    