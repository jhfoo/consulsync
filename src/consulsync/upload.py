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
  UpParser = subparser.add_parser(
    'up',
    help = 'Upload to Consul'
  )
  UpParser.add_argument('-s','--server')
  UpParser.add_argument('-d','--dir')
  UpParser.add_argument('-p','--path', default = '')
  UpParser.add_argument('-v','--debug', action = 'store_true', required = False)

# removes key and parent keys
def removeKey(keys, key):
  if key in keys:
    # print (f'[debug] removed key: {key}')
    del keys[key]

  if '/' in key:
    match = re.match(r'^(.*)\/(.+)', key)
    if match:
      ParentKey = match.group(1)
      # remove <parent>/
      ParentKeySlash = ParentKey + '/'
      if ParentKeySlash in keys:
        # print (f'[debug] removed key: {ParentKeySlash}')
        del keys[ParentKeySlash]

      # remove <parent>
      removeKey(keys, ParentKey)
      # print (f'match group 1: {}')


def upload(args):
  consul = util.getConsul(args.server)
  
  # print (f'- dir: {args.dir}')
  # sanity check
  if not os.path.isdir(args.dir):
    raise exceptions.PlannedException(f'Invalid path: {args.dir}')

  print (f'- Downloading existing keys')
  resp = consul.kv.get(args.path, recurse = True, keys = True)
  ExistingKeys = {key: None for key in resp[1]}
  print (ExistingKeys)

  PrefixLength = len(args.dir)
  for root, dirs, files in os.walk(args.dir):
    # print ('walk loop')
    # for DirName in dirs:
    #   print (f'root: {root}, dir: {DirName}')
    for file in files:
      with open(root + '/' + file, 'r') as infile:
        RootNoSlash = root[PrefixLength:]
        if RootNoSlash.startswith ('/'):
          key = RootNoSlash[1:]

        if key.startswith(args.path):
          # remove key from tracker
          removeKey(ExistingKeys, key)

          print (f'- key: {key}, file: {file}')
          data = yaml.safe_load(infile)
          # print (data)
          consul.kv.put(key, json.dumps(data, indent = 2))

  print (f'- Unused keys: {ExistingKeys.keys()}')
  # remove unused keys
  for key in ExistingKeys:
    consul.kv.delete(key)