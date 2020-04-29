#!/usr/bin/python

import os
import datetime
from math import pow, sqrt
import numpy as np
import uncertainties as unc
import xml.etree.ElementTree as et
from IOV import IOV
import itertools

class BeamSpot(object):
    '''
    BeamSpot object
    '''
    def __init__(self):
        self.Reset()
        
    def Reset(self):
        self.Type          = -1
        self.X             =  0.
        self.Xerr          =  0.
        self.Y             =  0.
        self.Yerr          =  0.
        self.Z             =  0.
        self.Zerr          =  0.
        self.sigmaZ        =  0.
        self.sigmaZerr     =  0.
        self.dxdz          =  0.
        self.dxdzerr       =  0.
        self.dydz          =  0.
        self.dydzerr       =  0.
        self.dxdy          =  0.
        self.dxdyerr       =  0.
        self.beamWidthX    =  0.
        self.beamWidthXerr =  0.
        self.beamWidthY    =  0.
        self.beamWidthYerr =  0.
        self.EmittanceX    =  0.
        self.EmittanceY    =  0.
        self.betastar      =  0.
        self.IOVfirst      =  0
        self.IOVlast       =  0
        self.IOVBeginTime  =  0
        self.IOVEndTime    =  0
        self.Run           =  0
        self.XYerr         =  0. 
        self.YXerr         =  0.
        self.dxdzdydzerr   =  0.
        self.dydzdxdzerr   =  0.
        self.sigmaXtrue    =  0.
        self.sigmaYtrue    =  0.        
        self.sigmaXtrueerr =  0.
        self.sigmaYtrueerr =  0.

        self.XPV           =  0.
        self.YPV           =  0.
        self.dxdzPV        =  0.
        self.dydzPV        =  0.
        self.PVcov         = np.zeros((9,9),dtype=np.double)        

        self.nPVs          =  0.
        self.FuncValue     =  0.

    def _computeProperWidths(self, full=False):
        '''
        Rotate back the covariance matrix by -dx/dz and -dy/dz.
        The sigma_x and sigma_y *of the luminous region itself* are set.
        The dx/dy rotation is not corrected (but it's small).
        The effect on sigma_z is neglected as it's small.
        '''
        if full:
            self._fullProperWidths()
        else:
            self._approximateProperWidths()

    def _fullProperWidths(self):
        '''
        full formula to compute the widths in the beam's reference frame.
        '''
        
        alpha = unc.ufloat(-self.dydz, self.dydzerr)
        beta  = unc.ufloat(-self.dxdz, self.dxdzerr)
    
        s_xx = unc.ufloat(np.power(self.beamWidthX, 2), np.power(self.beamWidthXerr, 2))
        s_yy = unc.ufloat(np.power(self.beamWidthY, 2), np.power(self.beamWidthYerr, 2))
        s_zz = unc.ufloat(np.power(self.sigmaZ    , 2), np.power(self.sigmaZerr    , 2))
                
        s_xz = beta  * (s_zz - s_xx) + alpha * unc.ufloat(self.XYerr, abs(self.XYerr)) # 100% uncertainty on XY correlation, as we don't save it...
        s_yz = alpha * (s_yy - s_zz) - beta  * unc.ufloat(self.XYerr, abs(self.XYerr)) # 100% uncertainty on XY correlation, as we don't save it...
        
        s_xx_true = s_xx - 2. * beta  * s_xz + np.power(beta , 2) * s_zz
        s_yy_true = s_yy + 2. * alpha * s_yz + np.power(alpha, 2) * s_zz
                
        self.sigmaXtrue = np.sqrt(max(0., s_xx_true.n))
        self.sigmaYtrue = np.sqrt(max(0., s_yy_true.n))
        
        self.sigmaXtrueerr = np.sqrt(max(0., s_xx_true.s))
        self.sigmaYtrueerr = np.sqrt(max(0., s_yy_true.s))

    def _approximateProperWidths(self):
        '''
        first order formula to compute the widths in the beam's reference frame.
        '''

        alpha = -self.dydz
        beta  = -self.dxdz

        s_xx = np.power(self.beamWidthX, 2)
        s_yy = np.power(self.beamWidthY, 2)
        s_zz = np.power(self.sigmaZ    , 2)
                        
        s_xx_true = s_xx - np.power(beta , 2) * s_zz
        s_yy_true = s_yy - np.power(alpha, 2) * s_zz
                
        self.sigmaXtrue = np.sqrt(max(0., s_xx_true))
        self.sigmaYtrue = np.sqrt(max(0., s_yy_true))
        
        # assume that the relative uncertainty on the proper widths is equal to that of the
        # transformed widths (approximately)
        self.sigmaXtrueerr = self.sigmaXtrue * self.beamWidthXerr / max(1.e-12, self.beamWidthX)
        self.sigmaYtrueerr = self.sigmaYtrue * self.beamWidthYerr / max(1.e-12, self.beamWidthY)

    def SetIOV(self, iov):
        '''
        Set BeamSpot interval of validity
        from an IOV object.
        Works only if the IOV spans over just *one* run.
        This descends from the way the BeamSpot thing is conceived.
        '''
        if iov.RunFirst != iov.RunLast:
            raise ValueError('First Run must be equal to last Run.\nNow first:'\
                             '%d\t last:%d' %(iov.RunFirst, iov.RunLast))
            exit()
            
        self.IOVBeginTime = iov.since
        self.IOVEndTime   = iov.till
        self.Run          = iov.RunFirst
        self.IOVfirst     = iov.LumiFirst
        self.IOVlast      = iov.LumiLast
        
    def GetIOV(self):
        '''
        Returns the interval of validity of the BeamSpot object.
        '''
        bsIOV = IOV()
        bsIOV.since     = self.IOVBeginTime
        bsIOV.till      = self.IOVEndTime
        bsIOV.RunFirst  = self.Run
        bsIOV.RunLast   = self.Run
        bsIOV.LumiFirst = self.IOVfirst
        bsIOV.LumiLast  = self.IOVlast
        
        return bsIOV
        
    def ReadXML(self, xml):
        '''
        Set the BeamSpot attributes from reading a xml file  or string 
        as returned by the condDB command:
        conddb dump 6601ff1538198fad046c18af4fb48ce3053e4c7c --format xml
        
        NotaBene: IOV boundaries are not saved in the xml from the DB
                  therefore they remain set to dummy values
        '''
        # check whether xml is a file or a xml-like string
        if os.path.isfile(xml):
            filein = open(xml) 
            lines = [line for line in filein.readlines() if 'DOCTYPE' 
                     not in line and 'boost_serialization' not in line]
        else:
            lines = [line for line in xml.split('\n') if 'DOCTYPE' 
                     not in line and 'boost_serialization' not in line]

        xmlstring = ''.join(lines)
                
        # get ahold of the xml object        
        dbentry = et.fromstring(xmlstring)
        
        # connect index to human readable names
        d = { k.tag.replace('-','') : i for i, k in enumerate(dbentry)}

        self.Xerr          = sqrt( float( dbentry[ d['covariance'] ].findall('item')[0].findall('item')[0].text ) )
        self.Yerr          = sqrt( float( dbentry[ d['covariance'] ].findall('item')[1].findall('item')[1].text ) )
        self.Zerr          = sqrt( float( dbentry[ d['covariance'] ].findall('item')[2].findall('item')[2].text ) )
        self.sigmaZerr     = sqrt( float( dbentry[ d['covariance'] ].findall('item')[3].findall('item')[3].text ) )
        self.dxdzerr       = sqrt( float( dbentry[ d['covariance'] ].findall('item')[4].findall('item')[4].text ) )
        self.dydzerr       = sqrt( float( dbentry[ d['covariance'] ].findall('item')[5].findall('item')[5].text ) )
        self.beamWidthXerr = sqrt( float( dbentry[ d['covariance'] ].findall('item')[6].findall('item')[6].text ) )
        self.beamWidthYerr = self.beamWidthXerr 

        self.Type          = int  ( dbentry[ d['type'      ] ].text                    )
        self.X             = float( dbentry[ d['position'  ] ].findall('item')[0].text )
        self.Y             = float( dbentry[ d['position'  ] ].findall('item')[1].text )
        self.Z             = float( dbentry[ d['position'  ] ].findall('item')[2].text )
        self.sigmaZ        = float( dbentry[ d['sigmaZ'    ] ].text                    )
        self.dxdz          = float( dbentry[ d['dxdz'      ] ].text                    )
        self.dydz          = float( dbentry[ d['dydz'      ] ].text                    )
        self.beamWidthX    = float( dbentry[ d['beamwidthX'] ].text                    )
        self.beamWidthY    = float( dbentry[ d['beamwidthY'] ].text                    )
        self.EmittanceX    = float( dbentry[ d['emittanceX'] ].text                    )
        self.EmittanceY    = float( dbentry[ d['emittanceY'] ].text                    )
        self.betastar      = float( dbentry[ d['betaStar'  ] ].text                    )

        self._computeProperWidths()

    def Read(self, payload):
        '''
        Reads the Payload-like fragment (portion of text file, from Run 
        to BetaStar) and sets its attributes accordingly.
        
        E.g.:
        
        Runnumber 195660
        BeginTimeOfFit 2012.06.07 07:22:30 GMT 1339053750
        EndTimeOfFit 2012.06.07 07:22:52 GMT 1339053772
        LumiRange 60 - 60
        Type 2
        X0 0.0720989
        Y0 0.0627524
        Z0 -1.19547
        sigmaZ0 4.76234
        dxdz 3.7475e-05
        dydz -2.86578e-05
        BeamWidthX 0.0020988
        BeamWidthY 0.00201228
        Cov(0,j) 4.35559e-08 3.11886e-10 0 0 0 0 0
        Cov(1,j) 3.11886e-10 4.63974e-08 0 0 0 0 0
        Cov(2,j) 0 0 0.0948918 0 0 0 0
        Cov(3,j) 0 0 0 0.0474358 0 0 0
        Cov(4,j) 0 0 0 0 1.76222e-09 2.11043e-11 0
        Cov(5,j) 0 0 0 0 2.11043e-11 1.773e-09 0
        Cov(6,j) 0 0 0 0 0 0 7.89321e-08
        EmittanceX 0.0
        EmittanceY 0.0
        BetaStar 0.0
        
        
        or -alternatively- it reads this format, which is what you get
        from what's dumped from the database
        
        
         for runs: 272760 - 272760
        -----------------------------------------------------
                      Beam Spot Data
        
         Beam type    = 2
               X0     = 0.0669316 +/- 0.000111673 [cm]
               Y0     = 0.0914736 +/- 0.00011168 [cm]
               Z0     = -0.188811 +/- 0.508985 [cm]
         Sigma Z0     = 2.48107 +/- 0.523828 [cm]
         dxdz         = 7.98489e-05 +/- 2.74296e-05 [radians]
         dydz         = 7.32328e-06 +/- 2.73298e-05 [radians]
         Beam Width X = 3.13566e-06 +/- 0.0216995 [cm]
         Beam Width Y = 4.14337e-06 +/- 0.0216995 [cm]
         Emittance X  = 0 [cm]
         Emittance Y  = 0 [cm]
         Beta star    = 0 [cm]
        '''
        
        if any(['Runnumber' in i for i in  payload]):
        
            self.Run           = int  ( payload[ 0].split()[1] )
            self.IOVBeginTime  = int  ( float(payload[ 1].split('GMT')[1]) )
            self.IOVEndTime    = int  ( float(payload[ 2].split('GMT')[1]) )
            self.IOVfirst      = int  ( payload[ 3].split()[1] )
            self.IOVlast       = int  ( payload[ 3].split()[3] )
            #self.IOVlast       = self.IOVfirst # DONT DO THIS
            self.Type          = int  ( payload[ 4].split()[1] )
    
            self.X             = float( payload[ 5].split()[1] )
            self.Y             = float( payload[ 6].split()[1] )
            self.Z             = float( payload[ 7].split()[1] )
    
            self.sigmaZ        = float( payload[ 8].split()[1] )
            self.dxdz          = float( payload[ 9].split()[1] )
            self.dydz          = float( payload[10].split()[1] )
    
            self.beamWidthX    = float( payload[11].split()[1] )
            self.beamWidthY    = float( payload[12].split()[1] )

            self.dxdy          = float( payload[13].split()[1] )
            
            # covariance matrix defined here
            # https://github.com/MilanoBicocca-pix/cmssw/blob/CMSSW_7_5_X_beamspot_workflow_riccardo/RecoVertex/BeamSpotProducer/src/PVFitter.cc#L306
            # diagonal terms 
            self.Xerr          = sqrt( float(payload[14].split()[1]) )
            self.Yerr          = sqrt( float(payload[15].split()[2]) )
            self.Zerr          = sqrt( float(payload[16].split()[3]) )
            self.sigmaZerr     = sqrt( float(payload[17].split()[4]) )
            self.dxdzerr       = sqrt( float(payload[18].split()[5]) )
            self.dydzerr       = sqrt( float(payload[19].split()[6]) )
            self.beamWidthXerr = sqrt( float(payload[20].split()[7]) )
            self.beamWidthYerr = sqrt( float(payload[21].split()[8]) )
            self.dxdyerr       = sqrt( float(payload[22].split()[9]) )
            
            # off diagonal terms
            self.XYerr         = float( payload[14].split()[2] )
            self.YXerr         = float( payload[15].split()[1] )
            self.dxdzdydzerr   = float( payload[18].split()[6] )
            self.dydzdxdzerr   = float( payload[19].split()[5] )

            # values from PV fit    
            self.XPV           = float( payload[23].split()[1] )
            self.YPV           = float( payload[24].split()[1] )
            self.dxdzPV        = float( payload[25].split()[1] )
            self.dydzPV        = float( payload[26].split()[1] )
            
            for icov in range(9):
                self.PVcov[icov]  = np.array(payload[27+icov].split()[1:10])

            self.EmittanceX    = float( payload[36].split()[1] )
            self.EmittanceY    = float( payload[37].split()[1] )
    
            self.betastar      = float( payload[38].split()[1] )    

            self.nPVs          = float( payload[39].split()[1] )
            self.FuncValue     = float( payload[40].split()[1] )

        if any(['Beam Spot Data' in i for i in  payload]):
            
            # FIXME! format changed!
            self.Run           = int  ( payload[ 0].split()[2]                               )
#             self.IOVfirst      = int  ( payload[ 0].split('LumiSection')[1].split()[0]       )
            self.IOVfirst      = int  ( payload[ 0].split('-')[-1]                           )
            self.IOVlast       = self.IOVfirst
            self.Type          = int  ( payload[ 4].split('=')[1]                            )
    
            self.X             = float( payload[ 5].split('=')[1].split('+/-')[0]            )
            self.Y             = float( payload[ 6].split('=')[1].split('+/-')[0]            )
            self.Z             = float( payload[ 7].split('=')[1].split('+/-')[0]            )
               
            self.sigmaZ        = float( payload[ 8].split('=')[1].split('+/-')[0]            )
            self.dxdz          = float( payload[ 9].split('=')[1].split('+/-')[0]            )
            self.dydz          = float( payload[10].split('=')[1].split('+/-')[0]            )
               
            self.beamWidthX    = float( payload[11].split('=')[1].split('+/-')[0]            )
            self.beamWidthY    = float( payload[12].split('=')[1].split('+/-')[0]            )

            self.dxdy          = float( payload[13].split('=')[1].split('+/-')[0]            )
            
            self.Xerr          = float( payload[ 5].split('=')[1].split('+/-')[1].split()[0] )
            self.Yerr          = float( payload[ 6].split('=')[1].split('+/-')[1].split()[0] )
            self.Zerr          = float( payload[ 7].split('=')[1].split('+/-')[1].split()[0] )
            self.sigmaZerr     = float( payload[ 8].split('=')[1].split('+/-')[1].split()[0] )
            
            self.dxdzerr       = float( payload[ 9].split('=')[1].split('+/-')[1].split()[0] )
            self.dydzerr       = float( payload[10].split('=')[1].split('+/-')[1].split()[0] )
            
            self.beamWidthXerr = float( payload[11].split('=')[1].split('+/-')[1].split()[0] )
            self.beamWidthYerr = float( payload[12].split('=')[1].split('+/-')[1].split()[0] )

            self.dxdyerr       = float( payload[13].split('=')[1].split('+/-')[1].split()[0] )
                
            self.EmittanceX    = float( payload[13].split('=')[1].split()[0]                 )
            self.EmittanceY    = float( payload[14].split('=')[1].split()[0]                 )

        self._computeProperWidths()

    def Dump(self, file, mode = 'a'):
        '''
        Dumps a Beam Spot objects into a Payload-like file.
        Default file open mode is append 'a', so that it can be serialised.
        '''
        
        f = open(file, mode)
        
        date_start = datetime.datetime.utcfromtimestamp(self.IOVBeginTime)
        date_end   = datetime.datetime.utcfromtimestamp(self.IOVEndTime  )
                
        str_date_start = '%d.%02d.%02d %02d:%02d:%02d' %( date_start.year   ,
                                                          date_start.month  ,
                                                          date_start.day    ,
                                                          date_start.hour   ,
                                                          date_start.minute ,
                                                          date_start.second )
        
        str_date_end   = '%d.%02d.%02d %02d:%02d:%02d' %( date_end.year   ,
                                                          date_end.month  ,
                                                          date_end.day    ,
                                                          date_end.hour   ,
                                                          date_end.minute ,
                                                          date_end.second )
        
        towrite = 'Runnumber {RUN}\n'                           \
                  'BeginTimeOfFit {DATESTART} GMT {TIMESTART}\n'\
                  'EndTimeOfFit {DATEEND} GMT {TIMEEND}\n'      \
                  'LumiRange {LUMISTART} - {LUMIEND}\n'         \
                  'Type {TYPE}\n'                               \
                  'X0 {X0}\n'                                   \
                  'Y0 {Y0}\n'                                   \
                  'Z0 {Z0}\n'                                   \
                  'sigmaZ0 {SZ0}\n'                             \
                  'dxdz {DXDZ}\n'                               \
                  'dydz {DYDZ}\n'                               \
                  'BeamWidthX {BWX}\n'                          \
                  'BeamWidthY {BWY}\n'                          \
                  'dxdy {DXDY}\n'                               \
                  'Cov(0,j) {M00} {M01} 0 0 0 0 0 0 0\n'            \
                  'Cov(1,j) {M10} {M11} 0 0 0 0 0 0 0\n'            \
                  'Cov(2,j) 0 0 {M22} 0 0 0 0 0 0\n'                \
                  'Cov(3,j) 0 0 0 {M33} 0 0 0 0 0\n'                \
                  'Cov(4,j) 0 0 0 0 {M44} {M45} 0 0 0\n'            \
                  'Cov(5,j) 0 0 0 0 {M54} {M55} 0 0 0\n'            \
                  'Cov(6,j) 0 0 0 0 0 0 {M66} 0 0\n'                \
                  'Cov(7,j) 0 0 0 0 0 0 0 {M77} 0\n'                \
                  'Cov(8,j) 0 0 0 0 0 0 0 0 {M88}\n'                \
                  ''.format(RUN       = str(self.Run          ),
                            DATESTART = str(str_date_start    ),
                            TIMESTART = str(self.IOVBeginTime ),
                            DATEEND   = str(str_date_end      ),
                            TIMEEND   = str(self.IOVEndTime   ),
                            LUMISTART = str(self.IOVfirst     ),
                            LUMIEND   = str(self.IOVlast      ),
                            TYPE      = str(self.Type         ),
                            X0        = str(self.X            ),
                            Y0        = str(self.Y            ),
                            Z0        = str(self.Z            ),
                            SZ0       = str(self.sigmaZ       ),
                            DXDZ      = str(self.dxdz         ),
                            DYDZ      = str(self.dydz         ),
                            DXDY      = str(self.dxdy         ),
                            BWX       = str(self.beamWidthX   ),
                            BWY       = str(self.beamWidthY   ),
                            # diagonal
                            M00       = str(pow(self.Xerr         , 2)),
                            M11       = str(pow(self.Yerr         , 2)),
                            M22       = str(pow(self.Zerr         , 2)),
                            M33       = str(pow(self.sigmaZerr    , 2)),
                            M44       = str(pow(self.dxdzerr      , 2)),
                            M55       = str(pow(self.dydzerr      , 2)),
                            M66       = str(pow(self.beamWidthXerr, 2)),
                            M77       = str(pow(self.beamWidthYerr, 2)),
                            M88       = str(pow(self.dxdyerr      , 2)),
                            #  off diagonal
                            M01       = str(self.XYerr        ),
                            M10       = str(self.YXerr        ),
                            M45       = str(self.dxdzdydzerr  ),
                            M54       = str(self.dydzdxdzerr  ),
                            )
        
        for i in range(9):
            towrite = towrite + 'PVCov(' + str(i) + ',j)'
            for j in range(9):
                towrite = towrite + ' {COVI}'.format(COVI = str(self.PVcov[i][j]))
            towrite = towrite + '\n'

        towrite = towrite + \
                  'xPV {XPV}\n'                          \
                  'yPV {YPV}\n'                          \
                  'dxdzPV {DXDZPV}\n'                    \
                  'dydzPV {DYDZPV}\n'                    \
                  'EmittanceX {EMX}\n'                   \
                  'EmittanceY {EMY}\n'                   \
                  'BetaStar {BSTAR}\n'                   \
                  'nPvs {NPVS}\n'                        \
                  'FuncValue {FUNCVALUE}\n'              \
                  ''.format(
                            XPV       = str(self.XPV          ),
                            YPV       = str(self.YPV          ),
                            DXDZPV    = str(self.dxdzPV       ),
                            DYDZPV    = str(self.dydzPV       ),
                            EMX       = str(self.EmittanceX   ),
                            EMY       = str(self.EmittanceY   ),
                            BSTAR     = str(self.betastar     ),
                            NPVS      = str(self.nPVs         ),
                            FUNCVALUE = str(self.FuncValue    ),
                            )
        f.write(towrite)




    def DumpCSV(self, file, mode = 'a'):
        '''
        Dumps a Beam Spot objects into a csv file.
        Default file open mode is append 'a', so that it can be serialised.
        '''
        
        f = open(file, mode)
     
        towrite = '{RUN} \t'                          \
                  '{TIMESTART} \t'                    \
                  '{TIMEEND} \t'                      \
                  '{TYPE} \t'                         \
                  '{X0} \t'                           \
                  '{X0Err} \t'                        \
                  '{Y0} \t'                           \
                  '{Y0Err} \t'                        \
                  '{Z0} \t'                           \
                  '{Z0Err} \t'                        \
                  '{SZ0} \t'                          \
                  '{SZ0Err} \t'                       \
                  '{DXDZ} \t'                         \
                  '{DXDZErr} \t'                      \
                  '{DYDZ} \t'                         \
                  '{DYDZErr} \t'                      \
                  '{DXDY} \t'                         \
                  '{DXDYErr} \t'                      \
                  '{BWX} \t'                          \
                  '{BWXErr} \t'                       \
                  '{BWY} \t'                          \
                  '{BWYErr} \t'                       \
                  '{TWX} \t'                          \
                  '{TWXErr} \t'                       \
                  '{TWY} \t'                          \
                  '{TWYErr} \t\n'      	              \
                  ''.format(RUN       = str(self.Run          ),
                            TIMESTART = str(self.IOVBeginTime ),
                            TIMEEND   = str(self.IOVEndTime   ),
                            TYPE      = str(self.Type         ),
                            X0        = str(self.X            ),
                            X0Err     = str(self.Xerr         ),
                            Y0        = str(self.Y            ),
                            Y0Err     = str(self.Yerr         ),
                            Z0        = str(self.Z            ),
                            Z0Err     = str(self.Zerr         ),
                            SZ0       = str(self.sigmaZ       ),
                            SZ0Err    = str(self.sigmaZerr    ),
                            DXDZ      = str(self.dxdz         ),
                            DXDZErr   = str(self.dxdzerr      ),
                            DYDZ      = str(self.dydz         ),
                            DYDZErr   = str(self.dydzerr      ),
                            DXDY      = str(self.dxdy         ),
                            DXDYErr   = str(self.dxdyerr      ),
                            BWX       = str(self.beamWidthX   ),
                            BWXErr    = str(self.beamWidthXerr),
                            BWY       = str(self.beamWidthY   ),
                            BWYErr    = str(self.beamWidthYerr),
                            TWX       = str(self.sigmaXtrue   ),
                            TWXErr    = str(self.sigmaXtrueerr),
                            TWY       = str(self.sigmaYtrue   ),
                            TWYErr    = str(self.sigmaYtrueerr),
                            )
        
        f.write(towrite)


    def DumpCSVFromPVFit(self, file, mode = 'a'):
        '''
        Dumps a Beam Spot objects into a csv file.
        Takes all values from the result of the PV fit.
        Prints central measurement and covariance matrix.
        '''
        
        f = open(file, mode)
     
        towrite = '{RUN} \t'                          \
                  '{TIMESTART} \t'                    \
                  '{TIMEEND} \t'                      \
                  '{TYPE} \t'                         \
                  '{X0} \t'                           \
                  '{Y0} \t'                           \
                  '{Z0} \t'                           \
                  '{SZ0} \t'                          \
                  '{DXDZ} \t'                         \
                  '{DYDZ} \t'                         \
                  '{DXDY} \t'                         \
                  '{BWX} \t'                          \
                  '{BWY} \t'                          \
                  ''.format(RUN       = str(self.Run          ),
                            TIMESTART = str(self.IOVBeginTime ),
                            TIMEEND   = str(self.IOVEndTime   ),
                            TYPE      = str(self.Type         ),
                            X0        = str(self.XPV          ),
                            Y0        = str(self.YPV          ),
                            Z0        = str(self.Z            ),
                            SZ0       = str(self.sigmaZ       ),
                            DXDZ      = str(self.dxdzPV       ),
                            DYDZ      = str(self.dydzPV       ),
                            DXDY      = str(self.dxdy         ),
                            BWX       = str(self.beamWidthX   ),
                            BWY       = str(self.beamWidthY   ),
#                             TWX       = str(self.sigmaXtrue   ),
#                             TWXErr    = str(self.sigmaXtrueerr),
#                             TWY       = str(self.sigmaYtrue   ),
#                             TWYErr    = str(self.sigmaYtrueerr),
                            )
        for j,k in itertools.product(range(9),range(9)):
            towrite = towrite + '{COVI} \t'.format(COVI = str(self.PVcov[j][k]))
        towrite = towrite + '{NPVS} \t {FUNCVALUE}'.format(NPVS = str(self.nPVs), FUNCVALUE = str(self.FuncValue))
        towrite = towrite + '\n'
        
        f.write(towrite)


    def __str__(self):
        '''
        Nice printer.
        '''
        toWrite = 'Run {} - LS {}-{}\n'\
                  'X0             = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'Y0             = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'Z0             = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'BeamWidthX     = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'BeamWidthY     = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'BeamWidthXTrue = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'BeamWidthYTrue = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'sigmaZ0        = {:3.6f} +/- {:3.4E} [cm]\n' \
                  'dxdz           = {:3.6E} +/- {:3.4E} [rad]\n'\
                  'dydz           = {:3.6E} +/- {:3.4E} [rad]'  \
                  .format(self.Run, str(self.IOVfirst), str(self.IOVlast),
                          self.X         , self.Xerr         ,
                          self.Y         , self.Yerr         ,
                          self.Z         , self.Zerr         ,
                          self.beamWidthX, self.beamWidthXerr,
                          self.beamWidthY, self.beamWidthYerr,
                          self.sigmaXtrue, self.sigmaXtrueerr,
                          self.sigmaYtrue, self.sigmaYtrueerr,
                          self.sigmaZ    , self.sigmaZerr    ,
                          self.dxdz      , self.dxdzerr      ,
                          self.dydz      , self.dydzerr      )
        return toWrite

 
    
       
if __name__ == '__main__':
#     mybs = BeamSpot()
#     myself.Dump('bs_dump_dummy.txt', 'w+')

    mybs = BeamSpot()
    mybs.ReadXML('/afs/cern.ch/work/m/manzoni/beamspot/CMSSW_7_5_0_pre4/src/RecoVertex/BeamSpotProducer/python/workflow/utils/payload_hash.xml')
    mybs.Dump('bs_dump_from_xml.txt', 'w+')
    print mybs
