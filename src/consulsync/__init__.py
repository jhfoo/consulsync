# core
import argparse
import os
import sys

sys.path.append(os.path.dirname(__file__))

# custom
import exceptions
import upload
import download
import version

def initArgParser():
  parser = argparse.ArgumentParser(
    prog = 'consulsync',
    description = 'Syncs files to Consul KV and vice verse'
  )
  parser.add_argument('-v', '--version', action='version', version='%(prog)s 2.0')
  subparser = parser.add_subparsers(dest='cmd')

  upload.addArgParser(subparser)
  download.addArgParser(subparser)
  version.addArgParser(subparser)

  SyncParser = subparser.add_parser(
    'sync',
    help = 'Sync to Consul'
  )
  SyncParser.add_argument('-d','--dir')


  return parser

def doCli():
  parser = initArgParser()
  args = parser.parse_args()

  try:
    # print (f'Working path: {os.getcwd()}')
    if args.cmd == None:
      parser.print_help()
    elif args.cmd == 'up':
      upload.upload(args)
    elif args.cmd == 'down':
      download.download(args)
    elif args.cmd == 'sync':
      pass
    elif args.cmd == 'ver':
      version.execArgs(args)
    else:
      print (args.cmd)  
  except exceptions.PlannedException as err:
    print (f'ERROR: {err}')
