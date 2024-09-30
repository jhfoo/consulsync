# core
import json
import os
import re

# community
import yaml

# custom
import exceptions
import util

def addArgParser(subparser):
  DownParser = subparser.add_parser(
    'down',
    help = 'Download to Consul'
  )
  DownParser.add_argument('-s','--server')
  DownParser.add_argument('-d','--dir')
  DownParser.add_argument('-p','--path', default = '')
  DownParser.add_argument('-r','--regex', required = False)
  DownParser.add_argument('-v','--debug', action = 'store_true', required = False)

def download(args):
  consul = util.getConsul(args.server)

  print (f'dir: {args.dir}')
  if args.regex:
    print (f'regex: {args.regex}')
    
  data = consul.kv.get(args.path,
    recurse = True)
  for item in data[1]:
    if not item['Value'] == None:
      if args.regex:
        pattern = re.compile(args.regex)
        if not re.search(pattern, item['Key']):
          continue

      # print (f"{item['Key']}: {item['Value']}")
      FullPath = args.dir + '/' + item['Key']
      print (f"- Key: {item['Key']}")
      # print (f"{item['Key']}: {json.loads(item['Value'].decode('utf-8'))}")
      os.makedirs(FullPath, exist_ok=True)
      with open(f'{FullPath}/data.yaml','w') as outfile:
        yaml.dump(json.loads(item['Value'].decode('utf-8')), outfile)

