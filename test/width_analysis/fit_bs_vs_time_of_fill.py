import os
import select
import ROOT
import math
import sys
# sys.path.append('..')

import numpy as np

from plot.CMSStyle import CMS_lumi
from collections   import namedtuple, OrderedDict
from array         import array
from itertools     import product
from ROOT          import TGraphErrors
ROOT.gROOT.SetBatch(True)

class Point():
    def __init__(self):
        self.fill    = -1.
        self.widthX  = -1.
        self.widthY  = -1.
        self.widthXe = -1.
        self.widthYe = -1.
        self.par1X   =  0.
        self.par1Xe  =  0.
        self.par2X   =  0.
        self.par2Xe  =  0.
        self.par1Y   =  0.
        self.par1Ye  =  0.
        self.par2Y   =  0.
        self.par2Ye  =  0.
    
    def ratio(self):
        return self.widthX/self.widthY
        
    def ratioerr(self):
        return math.sqrt( pow(self.widthXe/self.widthX,2) + pow(self.widthYe/self.widthY,2) ) * self.ratio()

    def uncX(self):
        return self.widthXe/self.widthX
    def uncY(self):
        return self.widthYe/self.widthY

    def __str__(self):
        return 'fill %d \t width X at t0 %.7f\t width Y at t0 %.7f \t ratio: %.7f' %(self.fill, self.widthX, self.widthY, self.ratio())
    
    
fit      = True
parabola = False

if parabola:
    outfolder = 'widths_vs_fill_allNovReReco_2017BF_parabolicFit_fromStable'
else:     
    outfolder = 'widths_vs_fill_allNovReReco_2017BF_linearFit_fromStable'

infile = ROOT.TFile('graphs_properWidth_perFill_fromStableBeam_allNovReReco_2017BF_firstPV_JetHT.root', 'read')

infile.cd()
dirList = ROOT.gDirectory.GetListOfKeys()

outfile = ROOT.TFile(outfolder + '/width_by_fill.root', 'recreate')
tree    = ROOT.TTree('tree', 'tree')

np_fill    = np.zeros(1, dtype=float)
np_widthX  = np.zeros(1, dtype=float)
np_widthEX = np.zeros(1, dtype=float)
np_widthY  = np.zeros(1, dtype=float)
np_widthEY = np.zeros(1, dtype=float)
np_ratio   = np.zeros(1, dtype=float)
np_ratioE  = np.zeros(1, dtype=float)
np_p1X     = np.zeros(1, dtype=float)
np_p1XE    = np.zeros(1, dtype=float)
np_p2X     = np.zeros(1, dtype=float)
np_p2XE    = np.zeros(1, dtype=float)
np_p1Y     = np.zeros(1, dtype=float)
np_p1YE    = np.zeros(1, dtype=float)
np_p2Y     = np.zeros(1, dtype=float)
np_p2YE    = np.zeros(1, dtype=float)

tree.Branch('fill'   , np_fill   , 'fill/D'   )
tree.Branch('widthX' , np_widthX , 'widthX/D' )
tree.Branch('widthEX', np_widthEX, 'widthEX/D')
tree.Branch('widthY' , np_widthY , 'widthY/D' )
tree.Branch('widthEY', np_widthEY, 'widthEY/D')
tree.Branch('ratio'  , np_ratio  , 'ratio/D'  )
tree.Branch('ratioE' , np_ratioE , 'ratioE/D' )
tree.Branch('p1X'    , np_p1X    , 'p1X/D'    )
tree.Branch('p1XE'   , np_p1XE   , 'p1XE/D'   )
tree.Branch('p2X'    , np_p2X    , 'p2X/D'    )
tree.Branch('p2XE'   , np_p2XE   , 'p2XE/D'   )
tree.Branch('p1Y'    , np_p1Y    , 'p1Y/D'    )
tree.Branch('p1YE'   , np_p1YE   , 'p1YE/D'   )
tree.Branch('p2Y'    , np_p2Y    , 'p2Y/D'    )
tree.Branch('p2YE'   , np_p2YE   , 'p2YE/D'   )

results = []


func = ROOT.TF1('thepol1', 'pol1', 0, 1000)
if parabola:
    func = ROOT.TF1('thepol2', 'pol2', 0, 1000)

ROOT.TGaxis.SetMaxDigits(3)

canvas_dict = OrderedDict()
for k1 in dirList: 
    graph = k1.ReadObj()
    ifill = int(graph.GetName()[4:8])
    ivar  = graph.GetName()[-1]
    graph.SetMarkerColor(ROOT.kRed*(ivar=='X') + ROOT.kBlue*(ivar=='Y'))
    graph.SetLineColor  (ROOT.kRed*(ivar=='X') + ROOT.kBlue*(ivar=='Y'))
    graph.SetMarkerStyle(8)
    graph.SetMarkerSize(.5)
    graph.SetTitle('')
    graph.GetXaxis().SetTitle(graph.GetXaxis().GetTitle() + ' %d'%ifill )
    func.SetLineColor(ROOT.kRed*(ivar=='X') + ROOT.kBlue*(ivar=='Y'))
    graph.Fit(func, 'R')
    chi2 = func.GetChisquare()
    if func.GetNDF() > 0:
        chi2n = func.GetChisquare()/func.GetNDF()
    else:
        chi2n = 0    
    prob = func.GetProb()
    if fit==False:
        width_0  = graph.GetY()[0]
        width_0e = graph.GetEY()[0]
        val = '   #sigma_{%s}(t=0) = %.3f #pm %.3f #mum'%(ivar,width_0*1E4, width_0e*1E4)
        slope    = 0
        slope_e  = 0
    else:
        width_0  = func.GetParameter(0)
        width_0e = func.GetParError(0)
        slope    = func.GetParameter(1)
        slope_e  = func.GetParError(1)
#         inc = width_0e/width_0          
#         val = '   #sigma_{%s}(t=0) = %.3f #pm %.3f #mum, #frac{d#sigma_{%s}}{dt} = %.3f #pm %.3f #mum/h, #chi^{2} = %.2f, #chi^{2}/NDOF = %.2f, prob = %.2f, inc=%.2f'%(ivar,width_0*1E4, width_0e*1E4, ivar, slope*1E4, slope_e*1E4, chi2, chi2n, prob*100, inc*100)
        val = '   #sigma_{%s}(t=0) = %.3f #pm %.3f #mum, #frac{d#sigma_{%s}}{dt} = %.3f #pm %.3f #mum/h'%(ivar,width_0*1E4, width_0e*1E4, ivar, slope*1E4, slope_e*1E4)
        if parabola:
            accel    = func.GetParameter(2)
            accel_e  = func.GetParError(2)
            val = '   #sigma_{%s}(t=0) = %.3f #pm %.3f #mum, #frac{d#sigma_{%s}}{dt} = %.3f #pm %.3f #mum/h, quadratic term = %.3f #pm %.3f #mum/h^{2}'%(ivar,width_0*1E4, width_0e*1E4, ivar, slope*1E4, slope_e*1E4, accel*1E4,  accel_e*1E4)
    try: 
        canvas_dict[ifill].cd()
        graph.Draw('P same')
        leg.AddEntry(graph, 'width%s'%ivar + val, 'pe')
#         leg.SetTextSize(0.023)
        leg.Draw()
        ROOT.gPad.Update()
        canvas_dict[ifill].SaveAs(outfolder + '/Fill%d'%ifill + '.pdf')
    except:
        canvas_dict[ifill] = ROOT.TCanvas('Fill_%d'%ifill, 'Fill_%d'%ifill, 600, 400)  
        canvas_dict[ifill].cd()
        graph.GetYaxis().SetTitle('beamspot width [cm]')
        graph.GetYaxis().SetTitleOffset(1.3)
        graph.Draw('AP')
        leg = ROOT.TLegend(0.25, 0.13, 0.85, 0.25)
        leg.SetBorderSize(0)
        leg.AddEntry(graph, 'width%s'%ivar + val, 'pe')
    
#     graph.GetXaxis().SetRangeUser(0., graph.GetXaxis().GetXmax())
    graph.GetXaxis().SetLimits(0., graph.GetXaxis().GetXmax())
    graph.GetYaxis().SetRangeUser(0.0001, 0.0015)
    ROOT.gPad.Update()
    CMS_lumi(ROOT.gPad, 4, 10)
    ROOT.gPad.Update()
    canvas_dict[ifill].Update()
    canvas_dict[ifill].Modified()
    
    append = True
    if [pp for pp in results if pp.fill==ifill]:
        mypoint = [pp for pp in results if pp.fill==ifill][0]
        append  = False
    else:
        mypoint = Point()
        mypoint.fill = ifill
    setattr(mypoint, 'width%s'  %ivar, width_0 )
    setattr(mypoint, 'width%se' %ivar, width_0e)
    setattr(mypoint, 'par1%s'   %ivar, slope   )
    setattr(mypoint, 'par1%se'  %ivar, slope_e )
    if parabola:
      setattr(mypoint, 'par2%s'   %ivar, func.GetParameter(2))
      setattr(mypoint, 'par2%se'  %ivar, func.GetParError(2) )
    else:
      setattr(mypoint, 'par2%s'   %ivar, 0. )
      setattr(mypoint, 'par2%se'  %ivar, 0. )

    if append:
        results.append(mypoint)


results.sort(key = lambda x : x.fill)
  
for iresults in results:
    np_fill    [0] = iresults.fill    
    np_widthX  [0] = iresults.widthX  
    np_widthEX [0] = iresults.widthXe  
    np_widthY  [0] = iresults.widthY 
    np_widthEY [0] = iresults.widthYe 
    np_ratio   [0] = iresults.ratio()
    np_ratioE  [0] = iresults.ratioerr()
    np_p1X     [0] = iresults.par1X   
    np_p1XE    [0] = iresults.par1Xe  
    np_p2X     [0] = iresults.par2X   
    np_p2XE    [0] = iresults.par2Xe  
    np_p1Y     [0] = iresults.par1Y   
    np_p1YE    [0] = iresults.par1Ye  
    np_p2Y     [0] = iresults.par2Y   
    np_p2YE    [0] = iresults.par2Ye  
    
    tree.Fill()  

outfile.cd()
tree.Write()
outfile.Close()

    
ratio  = []
fills  = []
eratio = []
efills = []

width_x   = []
ewidth_x  = []
width_y   = []
ewidth_y  = []

for i in results:
    if i.uncX() > 0.1 or i.uncY() > 0.1:  
        print ('will discard Fill', i.fill)
        continue
    ratio.append(i.ratio())
    fills.append(i.fill)
    eratio.append(i.ratioerr())
    efills.append(0.)
    width_x .append(i.widthX)
    ewidth_x.append(i.widthXe)
    width_y .append(i.widthY)
    ewidth_y.append(i.widthYe)
    
aratio  = array('f', ratio)
afills  = array('f', fills)     
aeratio = array('f', eratio)
aefills = array('f', efills)     

awidth_x  = array('f', width_x )     
aewidth_x = array('f', ewidth_x)     
awidth_y  = array('f', width_y )     
aewidth_y = array('f', ewidth_y)     


ROOT.TGaxis.SetMaxDigits(5)

c2    = ROOT.TCanvas('c2', 'c2', 1400, 800)
graphX = ROOT.TGraphErrors(len(afills), afills, awidth_x, aefills, aewidth_x)
graphY = ROOT.TGraphErrors(len(afills), afills, awidth_y, aefills, aewidth_y)

graphX.SetMarkerStyle(8)
graphX.SetMarkerColor(ROOT.kRed)
graphY.SetMarkerStyle(8)
graphY.SetMarkerColor(ROOT.kBlue)

graphX.SetTitle('')
graphX.Draw('AP')
graphX.GetXaxis().SetRangeUser(min(afills)-10, max(afills) +10)
graphX.GetYaxis().SetRangeUser(0.0001 , 0.002)
graphX.GetXaxis().SetTitle('LHC Fill')
graphX.GetYaxis().SetTitle('beamspot width at t=0 [cm]')
graphX.GetYaxis().SetTitleOffset(1.3)

graphY.Draw('P same')

leg2 = ROOT.TLegend(0.65, 0.7, 0.85, 0.88)
leg2.SetBorderSize(0)
leg2.AddEntry(graphX, 'sigma X', 'pel')
leg2.AddEntry(graphY, 'sigma Y', 'pel')
leg2.Draw()
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
CMS_lumi(ROOT.gPad, 4, 10)
ROOT.gPad.Update()

c2.SaveAs(outfolder + '/widths.pdf')




graph = ROOT.TGraphErrors(len(afills), afills, aratio, aefills, aeratio)
c1    = ROOT.TCanvas('c1', 'c1', 1400, 800)
graph.SetMarkerStyle(8)
graph.SetMarkerColor(ROOT.kAzure+1)
graph.SetLineColor(ROOT.kAzure+1)
graph.SetTitle('')
graph.Draw('AP')
graph.GetXaxis().SetRangeUser(min(afills)-10, max(afills) +10)
graph.GetYaxis().SetRangeUser(0.6, 1.4)
graph.GetXaxis().SetTitle('LHC Fill')
graph.GetYaxis().SetTitle('WidthX / WidthY')

line = ROOT.TLine(min(afills)-10, 1, max(afills)+10, 1)
line.SetLineColor(ROOT.kBlack)
line.Draw()
# graph.GetXaxis().SetRangeUser(0, abins[-1]+1000)
ROOT.gPad.Update()
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()

CMS_lumi(ROOT.gPad, 4, 10)
ROOT.gPad.Update()

c1.SaveAs(outfolder + '/ratio.pdf')
    

    
    
    
