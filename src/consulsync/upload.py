# core
import json
import os

# community
import yaml

# custom
import exceptions

def upload(args, consul):
  print (f'dir: {args.dir}')
  # sanity check
  if not os.path.isdir(args.dir):
    raise exceptions.PlannedException(f'Invalid path: {args.dir}')
  
  PrefixLength = len(args.dir)
  for root, dirs, files in os.walk(args.dir):
    # print ('walk loop')
    # for DirName in dirs:
    #   print (f'root: {root}, dir: {DirName}')
    for file in files:
      with open(root + '/' + file, 'r') as infile:
        RootNoSlash = root[PrefixLength:]
        if RootNoSlash.startswith ('/'):
          RootNoSlash = RootNoSlash[1:]

        print (f'root: {RootNoSlash}, file: {file}')
        data = yaml.safe_load(infile)
        print (data)
        consul.kv.put(RootNoSlash, json.dumps(data))
