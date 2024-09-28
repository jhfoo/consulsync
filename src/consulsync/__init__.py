# core
import argparse
import json
import os
import re
import sys

# community
import consul
import yaml

sys.path.append(os.path.dirname(__file__))

# custom
import exceptions
import upload

def download(args):
  print (f'dir: {args.dir}')
  if args.regex:
    print (f'regex: {args.regex}')
    
  data = con.kv.get(args.path,
    recurse = True)
  for item in data[1]:
    if not item['Value'] == None:
      if args.regex:
        pattern = re.compile(args.regex)
        if not re.search(pattern, item['Key']):
          continue

      # print (f"{item['Key']}: {item['Value']}")
      FullPath = args.dir + '/' + item['Key']
      print (f"{item['Key']}")
      # print (f"{item['Key']}: {json.loads(item['Value'].decode('utf-8'))}")
      os.makedirs(FullPath, exist_ok=True)
      with open(f'{FullPath}/data.yaml','w') as outfile:
        yaml.dump(json.loads(item['Value'].decode('utf-8')), outfile)


def doCli():
  con = consul.Consul(
    host='consul.service.consul'
  )

  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest='cmd')

  UpParser = subparser.add_parser(
    'up',
    help = 'Upload to Consul'
  )
  UpParser.add_argument('-d','--dir')
  UpParser.add_argument('-v','--debug', action = 'store_true', required = False)

  DownParser = subparser.add_parser(
    'down',
    help = 'Download to Consul'
  )

  args = parser.parse_args()
  if args.cmd == 'up':
    print (f'dir: {args.dir}')

  if args.cmd == 'down':
    print (f'dir: {args.dir}')

  print (args.cmd)

  DownParser.add_argument('-d','--dir')
  DownParser.add_argument('-p','--path', default = '')
  DownParser.add_argument('-r','--regex', required = False)

  SyncParser = subparser.add_parser(
    'sync',
    help = 'Sync to Consul'
  )


  args = parser.parse_args()
  try:
    print (f'Working path: {os.getcwd()}')
    if args.cmd == 'up':
      upload.upload(args, con)

    if args.cmd == 'down':
      download(args)

    if args.cmd == 'sync':
      pass

    print (args.cmd)  
  except exceptions.PlannedException as err:
    print (f'ERROR: {err}')
