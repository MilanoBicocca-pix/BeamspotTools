import os
import sys
sys.path.append('..')
from objects.Fill import Fill

'''
Dictionary to connect the number of (stable) LHC Fill to
the CMS run numbers.
For now this is periodically done by hand.
Could be made smarter at some point.

A handy re-labeling function is also provided.
'''

def _createFillList():
    
    fillDict = {}
    
#     fname = '/'.join( [os.environ['CMSSW_BASE'], 
#                        'src'                   , 
#                        'RecoVertex'            , 
#                        'BeamSpotProducer'      ,
#                        'python'                ,
#                        'BeamspotTools'         ,
#                        'data'                  ,
#                        'fills.txt'             ])

    fname = '/'.join( ['..', 
                       'data'                  ,
                       'fills.txt'             ])
        
    with open(fname) as f:
        content = f.readlines()
    
    for c in content[1:]:
        myFill = Fill()
        myFill.readLine(c)
        fillDict[myFill.Fill] = myFill
    
    return fillDict

fillDict = _createFillList()
fillRunDict = {k : v.Runs for k, v in fillDict.items()}

def labelByFill(histo):
  '''
  Takes a TH1.
  Relabels the x-axis so that the Fill number appears.
  '''
  for ibin in range(histo.GetNbinsX()):
    irun = histo.GetXaxis().GetBinLabel(ibin+1)
    if irun == '':  
      continue
    for k, v in fillRunDict.items():
      if int(irun) in v: 
        theifill = k
        break
    histo.GetXaxis().SetBinLabel(ibin+1, str(theifill))
  
  previousLabel = histo.GetXaxis().GetBinLabel(1)  
  for ibin in range(1, histo.GetNbinsX()):
    if histo.GetXaxis().GetBinLabel(ibin+1) == '':  continue
    if histo.GetXaxis().GetBinLabel(ibin+1) == previousLabel:
      histo.GetXaxis().SetBinLabel(ibin+1, '')
    else:
      previousLabel = histo.GetXaxis().GetBinLabel(ibin+1)

def labelByTime(histo, granularity = 1, fromRun = False):
    '''
    granularity
      0 --> years
      1 --> months
      2 --> weeks
      3 --> days
      4 --> hours
    to be implemented
    '''

    monthDict = {
        1  : 'January'  ,
        2  : 'February' ,
        3  : 'March'    ,
        4  : 'April'    ,
        5  : 'May'      ,
        6  : 'June'     ,
        7  : 'July'     ,
        8  : 'August'   ,
        9  : 'September',
        10 : 'October'  ,
        11 : 'November' ,
        12 : 'December' ,
    }
    
    if fromRun: 
        labelByFill(histo)
        
    creationYearPrecedent  = -99
    creationMonthPrecedent = -99
    creationDayPrecedent   = -99
    creationHourPrecedent  = -99
    
    for j, ibin in enumerate(range(histo.GetNbinsX())):

        ifill = histo.GetXaxis().GetBinLabel(ibin+1)        
                
        if ifill == '':  
            continue
            
        myfill = fillDict[int(ifill)]
        
        creationYear  = getattr(myfill.CreateTime, 'year' )        
        creationMonth = getattr(myfill.CreateTime, 'month')        
        creationDay   = getattr(myfill.CreateTime, 'day'  )        
        creationHour  = getattr(myfill.CreateTime, 'hour' )        
        
        if granularity==0 and creationYear == creationYearPrecedent:
            histo.GetXaxis().SetBinLabel(ibin + 1, '')
            continue

        if granularity==1 and creationMonth == creationMonthPrecedent:
            histo.GetXaxis().SetBinLabel(ibin + 1, '')
            continue

        if (granularity==2 or granularity==3) and creationDay == creationDayPrecedent:
            histo.GetXaxis().SetBinLabel(ibin + 1, '')
            continue

        if granularity==4 and creationHour == creationHourPrecedent:
            histo.GetXaxis().SetBinLabel(ibin + 1, '')
            continue


        if granularity == 0:
            creationTime = str(creationYear)

        if granularity == 1:
            if creationMonthPrecedent != creationMonth:
                creationTime = monthDict[creationMonth]
            else:
                creationTime = ''

        if granularity == 2:
            if creationMonthPrecedent != creationMonth:
                creationTime = str(creationDay) + ' ' + monthDict[creationMonth] + ' ---'
            elif creationDay%7==0:
                creationTime = str(creationDay)
            else:
                creationTime = ''

        if granularity == 3:
            if creationMonthPrecedent != creationMonth:
                creationTime = str(creationDay) + ' ' + monthDict[creationMonth] + ' ---'
            elif creationDayPrecedent != creationDay:
                creationTime = str(creationDay)
            else:
                creationTime == ''
        
        if granularity == 4:
            creationTime = '%d/%d - h%d' %(creationDay, creationMonth, creationHour)

        histo.GetXaxis().SetBinLabel(ibin + 1, str(creationTime))

        creationYearPrecedent  = creationYear 
        creationMonthPrecedent = creationMonth
        creationDayPrecedent   = creationDay  
        creationHourPrecedent  = creationHour 
 
 
def _splitByMagneticFieldJson(histo, json3p8, json2p8, json0, irun, frun):
    from RecoVertex.BeamSpotProducer.BeamspotTools.utils.readJson import readJson
    if json3p8: myjson3p8 = readJson(fileName = json3p8)
    if json2p8: myjson2p8 = readJson(fileName = json2p8)
    if json0  : myjson0   = readJson(fileName = json0  )
    
    runs3p8T  = sorted([i for i in myjson3p8.keys() if i >= irun and i <= frun])
    runs2p8T  = sorted([i for i in myjson2p8.keys() if i >= irun and i <= frun])
    runs0T    = sorted([i for i in myjson0  .keys() if i >= irun and i <= frun])
    runsOther = []

    histo0T = histo.Clone()
    histo0T.SetName(histo.GetName() + '0T')
    
    histo3p8T = histo.Clone()
    histo3p8T.SetName(histo.GetName() + '3p8T')

    histo2p8T = histo.Clone()
    histo2p8T.SetName(histo.GetName() + '2p8T')

    histoOther = histo.Clone()
    histoOther.SetName(histo.GetName() + 'Other')

    mydict = {
        histo0T   : runs0T   , 
        histo3p8T : runs3p8T ,
        histo2p8T : runs2p8T ,
        histoOther: runsOther,
    }
    
    for k, v in mydict.iteritems():
        k.Reset()
        add = False
        for ibin in range(k.GetNbinsX()):
            irun  = k.GetXaxis().GetBinLabel(ibin+1)
            binc  = histo.GetBinContent(ibin+1)
            bine  = histo.GetBinError  (ibin+1)
            if not irun:
                if add:
                    k.SetBinContent(ibin+1, binc)
                    k.SetBinError  (ibin+1, bine)
            elif int(irun) in v:
                k.SetBinContent(ibin+1, binc)
                k.SetBinError  (ibin+1, bine)
                add = True
            else:
                add = False
                    
    return histo0T, histo3p8T, histo2p8T, histoOther    


def _splitByMagneticFieldFill(histo):
    
    myFills = _createFillList()

    Fills3p8T  = []
    Fills0T    = []
    Fills2p8T  = []
    FillsOther = []

    for k, v in myFills.items():
        if v.Bfield > 3.7:
            Fills3p8T.append(k)
        elif v.Bfield < 0.1:
            Fills0T.append(k)
        elif v.Bfield > 2.7 and v.Bfield < 2.9:
            Fills2p8T.append(k)
        else:
            FillsOther.append(k)

    Fills3p8T .sort()
    Fills0T   .sort()
    Fills2p8T .sort()
    FillsOther.sort()
    
    histo0T = histo.Clone()
    histo0T.SetName(histo.GetName() + '0T')
    
    histo3p8T = histo.Clone()
    histo3p8T.SetName(histo.GetName() + '3p8T')

    histo2p8T = histo.Clone()
    histo2p8T.SetName(histo.GetName() + '2p8T')

    histoOther = histo.Clone()
    histoOther.SetName(histo.GetName() + 'Other')
    
    mydict = {
        histo0T   : Fills0T   , 
        histo3p8T : Fills3p8T ,
        histo2p8T : Fills2p8T ,
        histoOther: FillsOther,
    }
    
    for k, v in mydict.items():
        k.Reset()
        add = False
        for ibin in range(k.GetNbinsX()):
            ifill = k.GetXaxis().GetBinLabel(ibin+1)
            binc  = histo.GetBinContent(ibin+1)
            bine  = histo.GetBinError  (ibin+1)
            if not ifill:
                if add:
                    k.SetBinContent(ibin+1, binc)
                    k.SetBinError  (ibin+1, bine)
            elif int(ifill) in v:
                k.SetBinContent(ibin+1, binc)
                k.SetBinError  (ibin+1, bine)
                add = True
            else:
                add = False
                    
    return histo0T, histo3p8T, histo2p8T, histoOther    
    
      
def splitByMagneticField(histo, json = False, json3p8 = None, 
                         json2p8 = None, json0 = None, irun = -1, frun = 1E6):
    '''
    Gets a histogram with fills on the X axis and returns different histograms, 
    one for 0T fills, one for 3.8T fills one for 2.8T fills and 
    one for other fills. 
    '''
 
    if json:
        histo0T, histo3p8T, histo2p8T, histoOther = _splitByMagneticFieldJson(histo, json3p8, json2p8, json0, irun, frun)
    else:
        histo0T, histo3p8T, histo2p8T, histoOther = _splitByMagneticFieldFill(histo)
    
    return histo0T, histo3p8T, histo2p8T, histoOther    



        








