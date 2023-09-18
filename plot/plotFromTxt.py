'''
blame: Luca Guzzi INFN Milano-Bicocca
on: august 2023
'''
import sys, time, os
assert sys.version_info.major>2, "This script requires python 3+"
import ROOT
import uncertainties
import multiprocessing as mp
from datetime import datetime
from array import array
import http.cookiejar as cookielib
import requests

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)

def get_cookie(url):
  '''generate a cookie for the OMS website
  '''
  cookiepath = './.cookiefile_OMSfetch.txt'
  print("[INFO] generating cookie for url", url)
  cmd = 'auth-get-sso-cookie --url "{}" -o {}'.format(url, cookiepath)
  ret = os.system(cmd)
  cookie = cookielib.MozillaCookieJar(cookiepath)
  cookie.load()
  os.remove(cookiepath)
  return cookie

def fetch_data(url, cookie):
  '''make a request to the OMS website and filter stable-beam proton-proton entries
  '''
  req = requests.get(url, verify=True, cookies=cookie, allow_redirects=False)
  if not req.ok:
    return []
  jsn = req.json()
  if not 'data' in jsn.keys():
    return []
  return jsn

progress = mp.Value('f', 0., lock=True)
def pbar():
  '''print a progressbar
  '''
  global progress
  bar = lambda dim=50: '[{}{}%{}]'.format('#'*int(progress.value*dim/100+1), int(progress.value), ' '*int(dim-progress.value*dim/100+1))
  while(True):
    dim=min(50, os.get_terminal_size()[0]-10)
    sys.stdout.write('\r%s' %bar(dim))
    sys.stdout.flush()
    time.sleep(.1)
    if progress.value == 100:
      break
  sys.stdout.write('\r%s\n' %bar(dim))
  sys.stdout.flush()

class BeamspotFile:
  ''' class for handling beamspot parsing on multiple files
  '''
  manager = mp.Manager()
  COOKIE=get_cookie('https://cmsoms.cern.ch/')
  TOPLOT  = {
    'x'     : 'beam spot x [cm]'      ,
    'y'     : 'beam spot y [cm]'      ,
    'z'     : 'beam spot z [cm]'      ,
    'widthX': 'beam spot #sigma_x [cm]',
    'widthY': 'beam spot #sigma_y [cm]',
    'widthZ': 'beam spot #sigma_z [cm]',
    'dxdz'  : 'beam spot dx/dz'       ,
    'dydz'  : 'beam spot dy/dz'
  }
  URL     = "https://cmsoms.cern.ch/agg/api/v1/{K}/{ID}/"
  CANFAIL = False
  @staticmethod
  def format_graph(graph, color):
    graph.SetMarkerStyle(8)
    graph.SetMarkerSize(0.3)
    graph.SetLineColor(color)
    graph.SetMarkerColor(color)
    graph.GetYaxis().SetTitleOffset(1.5)
    #graph.GetYaxis().SetRangeUser(mymin, mymax)
    #graph.SetLabelSize(0.075, 'XY')
  @staticmethod
  def format_canvas(canvas):
    canvas.SetGridx()
    canvas.SetGridy()
    canvas.SetBottomMargin(0.1)
  @staticmethod
  def fetch_from_OMS(entry):
    '''core function, fetches data from OMS in a way which is parallelizable 
    through a mulitprocessing pool
    '''
    toepoch = lambda tme: (datetime.strptime(tme, "%Y-%m-%dT%H:%M:%SZ")-datetime(1970,1,1)).total_seconds()
    run, ls, le, length = entry
    runjsn  = fetch_data(cookie=BeamspotFile.COOKIE, url=BeamspotFile.URL.format(K='runs'         , ID=run))
    lsjsn   = fetch_data(cookie=BeamspotFile.COOKIE, url=BeamspotFile.URL.format(K='lumisections' , ID='_'.join([str(run), str(ls)])))
    lejsn   = fetch_data(cookie=BeamspotFile.COOKIE, url=BeamspotFile.URL.format(K='lumisections' , ID='_'.join([str(run), str(le)]))) if le!=ls else lsjsn
    filljsn = fetch_data(cookie=BeamspotFile.COOKIE, url=BeamspotFile.URL.format(K='fills'        , ID=runjsn['data']['attributes']['fill_number']))
    beamspot = {}
    beamspot[(run,ls,le)] = {}
    beamspot[(run,ls,le)]['fill'     ] = filljsn['data']['id']
    beamspot[(run,ls,le)]['fillstamp'] = toepoch(filljsn['data']['attributes']['start_time'])
    beamspot[(run,ls,le)]['date'     ] = lsjsn['data']['attributes']['start_time'] 
    beamspot[(run,ls,le)]['timestamp'] = 0.5*(
      toepoch(lejsn['data']['attributes']['end_time'  ]) +
      toepoch(lsjsn['data']['attributes']['start_time'])
    )
    beamspot[(run,ls,le)]['timewidth'] = (
      toepoch(lejsn['data']['attributes']['end_time'  ]) -
      toepoch(lsjsn['data']['attributes']['start_time'])
    )
    progress.value += 100./length
    return beamspot

  def __init__(self, file, color=ROOT.kBlack):
    #this snippet will read the diabolic beamspot file format
    self.color = color
    with open(file, 'r') as ifile:
      self.beamspots = BeamspotFile.manager.dict({#key: (run, ls_begin, ls_end)
        ( int(lines[0]              ), 
          int(lines[3].split(' ')[1]), 
          int(lines[3].split(' ')[3])): {
          'beginTime' : int   (lines[1] .split(' ')[-1]),
          'endTime'   : int   (lines[2] .split(' ')[-1]),
          'fittype'   : int   (lines[4] .split(' ')[-1]),
          'x'         : float (lines[5] .split(' ')[-1]),
          'y'         : float (lines[6] .split(' ')[-1]),
          'z'         : float (lines[7] .split(' ')[-1]),
          'widthZ'    : float (lines[8] .split(' ')[-1]),
          'dxdz'      : float (lines[9] .split(' ')[-1]),
          'dydz'      : float (lines[10].split(' ')[-1]),
          'widthX'    : float (lines[11].split(' ')[-1]),
          'widthY'    : float (lines[12].split(' ')[-1]),
          'emittanceX': float (lines[20].split(' ')[-1]),
          'emittanceY': float (lines[21].split(' ')[-1]),
          'betaStar'  : float (lines[22].split(' ')[-1]),
          'covariance': [[float(e) for e in row.split(' ')[1:] if len(e)] for row in lines[13:20]],
        } for lines in [d.split('\n') for d in ifile.read().split('Runnumber ') if len(d)]
        if int(lines[4] .split(' ')[-1])==2 or BeamspotFile.CANFAIL
      })

    print("[INFO]fetching data from OMS for", file)
    with mp.Pool(args.streams) as pool:
      progressbar = mp.Process(target=pbar)
      progressbar.start()
      fetched = pool.map(BeamspotFile.fetch_from_OMS, [(run,ls,le,len(self.beamspots.keys())) for run,ls,le in self.beamspots.keys()])
      progressbar.terminate()
    print()
    progress.value = 0.0
    fetched = {k: v for d in fetched for k,v in d.items()}
    for k in fetched.keys():
      self.beamspots[k] = {**self.beamspots[k], **fetched[k]}
    self.graphs = {
      v: ROOT.TGraph(len(self.beamspots.keys()),
        array('d', [bs['timestamp']  for bs in self.beamspots.values()]),
        array('d', [bs[v]            for bs in self.beamspots.values()]),
      ) 
      for v in BeamspotFile.TOPLOT.keys()
    }
  @staticmethod
  def plot(entries, outputdir):
    os.makedirs(outputdir, exist_ok=True)
    for v, lab in BeamspotFile.TOPLOT.items():
      can = ROOT.TCanvas('c1', 'c1', 1400, 800)
      BeamspotFile.format_canvas(can)
      mul = ROOT.TMultiGraph()
      leg = ROOT.TLegend()
      mul.SetTitle('beamspot {V} vs. time;epoch;{L}'.format(V=v,L=lab))
      for i, entry in enumerate(entries):
        BeamspotFile.format_graph(entry.graphs[v], entry.color)
        entry.graphs[v].SetMarkerStyle(20)
        leg.AddEntry(entry.graphs[v], '', 'lep')
        mul.Add(entry.graphs[v])
      mul.Draw("AP")
      can.SaveAs("{O}/{V}.pdf".format(O=outputdir,V=v), "pdf")

if __name__=='__main__':
  import argparse
  parser = argparse.ArgumentParser('''
  This script plots the beamspot parameters as a function of the lumisection.
  It uses kerberos to fetch time data from OMS.
  The code works with an input file list and 
  can overlay multiple beamspots for comparison.
  WIP. TODOs:
  - format the canvas as the standard BS file
  - improve the readability and simplify where possible
  ''')
  parser.add_argument('--input'   , required=True, nargs='+', help='list of input files')
  parser.add_argument('--output'  , required=True           , help='output directory')
  parser.add_argument('--streams' , default=1, type=int     , help='number of streams for the OMS data download')
  parser.add_argument('--canfail' , action='store_true'     , help='use only type 2 (good) fits')
  args = parser.parse_args()
  
  BeamspotFile.CANFAIL = args.canfail

  BeamspotFile.plot([
    BeamspotFile(file=file) for file in args.input
  ], outputdir=args.output)
