from CRABClient.UserUtilities import config as Configuration
from CRABAPI.RawCommand import crabCommand

import os
import json
import argparse
parser = argparse.ArgumentParser('''Submit jobs to skim events for VdM tasks.\n
The script reads time ranges, run ranges and lumisections from LUMI json files. 
The bunch crossings list is provided as an external argument.\n
Each submission should correspond to a single dataset and a single VdM configuration (json file).\n
The output consists of events falling in the time ranges specified in the json file, 
matching the given bunch crossing numbers.
''')
parser.add_argument('--input'         , required=True             , help='timestamp file from lumi')
parser.add_argument('--storage'       , default='T3_IT_MIB'       , help='storage site')
parser.add_argument('--dataset'       , required=True             , help='input dataset')
parser.add_argument('--bunchcrossings', required=True             , help='list of bunchcrossings to select', nargs='+')
parser.add_argument('--workarea'      , default='TimeBX_skim'     , help='crab work area')
parser.add_argument('--dryrun'        , action='store_true'       , help='don\'t run CRAB')
args = parser.parse_args()

class Scan:
  '''main class for building a scan object from a LUMI POG json file.
  A Scan instance identifies a particular scan effort (eg. diagonal X coordinate).
  '''
  def __init__(self, label, json, number):
    self.label  = os.path.basename(label).strip('.json')
    self.main   = json
    self.index  = number
    self.scan   = self.main['Scans'][self.index]
    self.fill   = self.main['Fill'     ]
    self.runn   = self.main['Run'      ][self.index]
    self.stype  = self.main['ScanTypes'][self.index]
    self.sname  = self.main['ScanNames'][self.index]
    self.name   = '_'.join([
      self.label, 
      str(self.fill), 
      str(self.runn), 
      self.stype, 
      self.sname])
    self.points = [Point(scan=self, index=i) for i in range(self.scan['NumPoints'])]
    self.runs   = ','.join(p.runs   for p in self.points)
    self.times  = ','.join(p.times  for p in self.points)

class Point:
  ''' class for building a scan point object. 
  A Point instance identifies a beam step in a scan effort.
  '''
  QUERYBLOCK = 'dasgoclient --query="block run={R} dataset={D}"'
  def __init__(self, scan, index):
    self.scan     = scan
    self.index    = index
    self.lumib    = self.scan.scan['LSStartTimes'][self.index]
    self.lumie    = self.scan.scan['LSStopTimes' ][self.index]
    self.timeb    = self.scan.scan['StartTimes'  ][self.index]
    self.timee    = self.scan.scan['StopTimes'   ][self.index]
    self.runs     = '{R}:{B}-{R}:{E}'.format(R=self.scan.runn, B=self.lumib, E=self.lumie)
    self.times    = '{B}:{E}'.format(B=self.timeb, E=self.timee)
    self.name     = '_'.join([
      self.scan.name,
      str(self.lumib),
      str(self.lumie),
      str(self.index)])
    self.blocks   = self.get_blocks()
  def get_blocks(self):
    return [l.strip('\n') for l in os.popen(Point.QUERYBLOCK.format(R=self.scan.runn, D=args.dataset))]

lumijson  = json.load(open(args.input, 'r'))
scans     = [Scan(label=os.path.basename(args.input).strip('.json'), json=lumijson, number=s['ScanNumber']-1) for s in lumijson['Scans']]
import pdb; pdb.set_trace()
JOBNAME     = '_'.join([args.dataset.split('/')[1], os.path.basename(args.input).strip('.json')])
RUNSTRING   = ','.join(s.runs   for s in scans)
TIMESTRING  = ','.join(s.times  for s in scans)
BUNCHSTRING = ','.join(b for b in args.bunchcrossings)
OUTPUT      = '/store/user/{}/BeamSpot/'.format(os.environ['USER'])

config = Configuration()
config.General.workArea         = args.workarea
config.General.requestName      = JOBNAME
config.General.transferOutputs  = True
config.JobType.pluginName       = 'Analysis'
config.Data.publication         = False
config.Data.useParent           = False
config.Data.inputDBS            = 'global'
config.Data.splitting           = 'FileBased' if args.dryrun else 'Automatic'
config.Data.unitsPerJob         = 2700
config.Data.inputDataset        = args.dataset
config.Data.runRange            = RUNSTRING
config.Site.storageSite         = args.storage
config.JobType.psetName         = 'EventSkimming_byTime_byBX.py'
config.JobType.pyCfgParams = [
  "bunchcrossing={}".format(BUNCHSTRING),
  "timerange={}"    .format(TIMESTRING) ,
]
#config.Data.outLFNDirBase       = '/
crabCommand('submit', config=config, dryrun=args.dryrun)