# core
import argparse



def doCli():
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest='cmd')

  UpParser = subparser.add_parser(
    'up',
    help = 'Upload to Consul'
  )
  UpParser.add_argument('-d','--dir')

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