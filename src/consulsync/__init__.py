# core
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__))

# custom
import exceptions
import upload
import download

def initArgParser():
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest='cmd')

  upload.addArgParser(subparser)
  download.addArgParser(subparser)

  SyncParser = subparser.add_parser(
    'sync',
    help = 'Sync to Consul'
  )
  SyncParser.add_argument('-d','--dir')

  args = parser.parse_args()
  return args

def doCli():
  args = initArgParser()

  try:
    print (f'Working path: {os.getcwd()}')
    if args.cmd == 'up':
      upload.upload(args)
    elif args.cmd == 'down':
      download.download(args)
    elif args.cmd == 'sync':
      pass
    else:
      print (args.cmd)  
  except exceptions.PlannedException as err:
    print (f'ERROR: {err}')
