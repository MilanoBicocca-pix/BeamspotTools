'''
blame: Luca Guzzi INFN Milano-Bicocca
on: august 2023
'''
import sys
assert sys.version_info.major>2, "This script requires python 3+"
import ROOT
import uncertainties
import os
import http.cookiejar as cookielib
import requests
import multiprocessing as mp
from datetime import datetime

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
COOKIE=get_cookie('https://cmsoms.cern.ch/')

def fetch_data(url):
  global COOKIE
  req = requests.get(url, verify=True, cookies=COOKIE, allow_redirects=False)
  if not req.ok: return {}
  jsn = req.json()
  if not 'data' in jsn.keys(): return {}
  return jsn

class BeamspotFile:
  ''' singleton for handling beamspot parsing on multiple files
  '''
  TOPLOT  = ['x','y','z','widthX','widthY','widthZ','dxdz','dydx']
  URL     = "https://cmsoms.cern.ch/agg/api/v1/{K}/{ID}/"
  def __init__(self, ifile):
    #this snippet will read the diabolic beamspot file format
    with open(ifile, 'r') as ifile:
      self.beamspots = {#key: (run, ls_begin, ls_end)
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
      }
    # here we fetch lumisection information from OMS and 
    # compute the timestamp for each one
    toepoch = lambda tme: (datetime.strptime(tme, "%Y-%m-%dT%H:%M:%SZ")-datetime(1970,1,1)).total_seconds()
    for run,ls,le in self.beamspots.keys():
      runjsn  = fetch_data(url=BeamspotFile.URL.format(K='runs'         , ID=run))
      lsjsn   = fetch_data(url=BeamspotFile.URL.format(K='lumisections' , ID='_'.join([str(run), str(ls)])))
      lejsn   = fetch_data(url=BeamspotFile.URL.format(K='lumisections' , ID='_'.join([str(run), str(le)]))) if le!=ls else lsjsn
      filljsn = fetch_data(url=BeamspotFile.URL.format(K='fills'        , ID=runjsn['data']['attributes']['fill_number']))
      self.beamspots[(run,ls,le)]['fill'     ] = filljsn['data']['id']
      self.beamspots[(run,ls,le)]['fillstamp'] = toepoch(filljsn['data']['attributes']['start_time'])
      self.beamspots[(run,ls,le)]['date'     ] = lumijsn[(run,ls)]['attributes']['start_time'] 
      self.beamspots[(run,ls,le)]['timestamp'] = 0.5*(
        toepoch(lumijsn[(run, le)]['attributes']['end_time'  ]) +
        toepoch(lumijsn[(run, ls)]['attributes']['start_time'])
      )
      self.beamspots[(run,ls,le)]['timewidth'] = (
        toepoch(lumijsn[(run, le)]['attributes']['end_time'  ]) -
        toepoch(lumijsn[(run, ls)]['attributes']['start_time'])
      )
    
    def graph(self):
      '''create graphs of the beamspot entries
      '''
      graphs = {v: ROOT.TGraphErrors() for v in BeamspoFile.TOPLOT}

if __name__=='__main__':
  import argparse
  parser = argparse.ArgumentParser('''
  This script plots the beamspot parameters as a function of the lumisection.
  It uses kerberos to fetch time data from OMS.
  The code works with an input file list and 
  can overlay multiple beamspots for comparison.
  WIP. TODOs:
  - implement plotting
  - format the canvas as the standard BS file
  - improve the readability and simplify where possible
  ''')
  parser.add_argument('--input', required=True, nargs='+')
  args = parser.parse_args()
  
  beamspot_entries = [
    BeamspotFile(ifile=ifile) for ifile in args.input
  ]
