#!/usr/bin/env python3
from __future__ import print_function
import sys
assert sys.version_info.major>2, "This script requires python 3+"
import os
assert os.system("auth-get-sso-cookie --help &> /dev/null")==0, "auth-get-sso-cookie must be installed. You should run this script on lxplus"
import time
import json
import requests
import http.cookiejar as cookielib
import multiprocessing as mp

import argparse
parser = argparse.ArgumentParser('''
This script fetches information about stable proton fills form OMS and saves them in a txt file.
Fills are fetched starting from most recent one.''')
parser.add_argument('-n', '--number-of-fills', default=100                      , help="Number of fills to fetch"                     , type=int)
parser.add_argument('-u', '--update'         , default=None                     , help="File to update"                               , type=str)
parser.add_argument('-o', '--output'         , default='output.txt'             , help="Output file"                                  , type=str)
parser.add_argument('-s', '--streams'        , default=max(mp.cpu_count()-4, 1) , help="Number of streams to use for fetching data"   , type=int)
parser.add_argument('-S', '--size'           , default=100                      , help="Number of fills to fetch with a single stream", type=int)
args = parser.parse_args()

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

def fetch_data(url):
  '''make a request to the OMS website and filter stable-beam proton-proton entries
  '''
  global COOKIE
  req = requests.get(url, verify=True, cookies=COOKIE, allow_redirects=False)
  if not req.ok:
    return []
  jsn = req.json()
  if not 'data' in jsn.keys():
    return []
  jsn = [j for j in jsn['data'] if not j['attributes']['fill_type_runtime'] is None and 'PROTONS' in j['attributes']['fill_type_runtime']]
  jsn = [j for j in jsn if j['attributes']['stable_beams' if 'stable_beams' in j['attributes'].keys() else 'stable_beam']]
  return jsn

def get_fills(url):
  '''fetch the fills from OMS and the corresponding collision runs
  '''
  global chunks
  fills = fetch_data(url)
  runs  = [fetch_data(f['relationships']['runs']['links']['related']) for f in fills]
  
  fills = [f['attributes'] for f in fills]
  runs  = [' '.join([run['id'] for run in r if not run['attributes']['l1_hlt_mode'] is None and 'collisions' in run['attributes']['l1_hlt_mode']]) for r in runs]
  
  for i, f in enumerate(fills):
    f['runs'] = runs[i]
  fills = [f for f in fills if len(f['runs'])]
  
  progress.value += 100. / len(chunks)
  time.sleep(.5)
  return fills

progress = mp.Value('f', 0., lock = True)
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

STEP=100
URL="https://cmsoms.cern.ch/agg/api/v1/fills/?sort=-start_time&page[offset]={OFF}&page[limit]={LIM}"
COOKIE=get_cookie('https://cmsoms.cern.ch/')

print('[INFO] Fetching data from OMS')
chunks = sorted(set([_ for _ in range(0, args.number_of_fills, args.size)]+[args.number_of_fills]))
with mp.Pool(args.streams) as pool:
  progressbar = mp.Process(target=pbar)
  progressbar.start()
  fetched = pool.map(get_fills, [URL.format(OFF=off, LIM=args.size) for off in chunks])
  progressbar.terminate()

if args.update is not None:
  with open(args.update, 'r') as ifile:
    oldmessage = [l.strip('\n') for l in ifile.readlines()[1:]]
    oldfills   = [int(l.split('\t')[0]) for l in oldmessage if len(l)]
else:
  oldfills    = []
  oldmessage  = []

fills = [f for fetch in fetched for f in fetch if f['fill_number'] not in oldfills]
print('[INFO]', len(fills), 'fills fetched.')

format_time     = lambda time      : str(time).replace('T', ' ').replace('Z', '').replace('-', '.')
format_seconds  = lambda seconds   : time.strftime('%H hr %M min', time.gmtime(seconds)) if seconds is not None else str(None)
format_runs     = lambda start, end: ' '.join([str(r) for r in range(start, end+1)]) if None not in [start,end] else str(None)
header_map = {
  'Fill'              : lambda dic: dic['fill_number']                    ,
  'Create Time'       : lambda dic: format_time(dic['start_time'])        , # NOTE: this is the start time, not the stable beam start time
  'Duration Stable'   : lambda dic: format_seconds(dic['duration'])       , # NOTE: 'duration' indicates the stable beam duration
  'Bfield'            : lambda dic: dic['b_field']                        ,
  'Peak Inst Lumi'    : lambda dic: dic['peak_lumi']                      ,
  'Peak Pileup'       : lambda dic: dic['peak_pileup']                    ,
  'Peak Spec Lumi'    : lambda dic: dic['peak_specific_lumi']             ,
  'Delivered Lumi'    : lambda dic: dic['delivered_lumi']                 ,
  'Recorded Lumi'     : lambda dic: dic['recorded_lumi']                  ,
  'Eff By Lumi'       : lambda dic: dic['efficiency_lumi']                ,
  'Eff By Time'       : lambda dic: dic['efficiency_time']                ,
  'Begin Time'        : lambda dic: format_time(dic['start_stable_beam']) , # NOTE: this is the stable beam start time, not the start time
  'to Ready'          : lambda dic: dic['to_ready_time']                  , # OMS: "to HV on" [s]
  'End Time'          : lambda dic: format_time(dic['end_stable_beam'])   , # NOTE: this is the stable beam end time, not the end time
  'Type'              : lambda dic: dic['fill_type_runtime']              ,
  'Energy'            : lambda dic: dic['energy']                         ,
  'I Beam1 (x10^11)'  : lambda dic: dic['intensity_beam1']                ,
  'I Beam2 (x10^11)'  : lambda dic: dic['intensity_beam2']                ,
  'nB1'               : lambda dic: dic['bunches_beam1']                  ,
  'nB2'               : lambda dic: dic['bunches_beam2']                  ,
  'nCol'              : lambda dic: dic['bunches_colliding']              ,
  'nTar'              : lambda dic: dic['bunches_target']                 ,
  'xIng (micro rad)'  : lambda dic: dic['crossing_angle']                 ,
  'Injection Scheme'  : lambda dic: dic['injection_scheme']               ,
  'Runs'              : lambda dic: dic['runs']                           ,
  'Comments'          : lambda dic: ''                                    ,
}

header      = ['\t'.join(header_map.keys())]
newmessage  = ['\t'.join([str(val(fill)) for val in header_map.values()]) for fill in fills]
message     = '\n'.join(header+newmessage+oldmessage)

with open(args.output, 'w') as ofile:
  ofile.write(message)
