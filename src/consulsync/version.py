# core
import re

# community
import semver
import toml

def addArgParser(subparser):
  VersionParser = subparser.add_parser(
    'ver',
    help = 'Bump release version for build'
  )
  VersionParser.add_argument(
    'mode', 
    nargs = '?', 
    default = 'info',
    help = 'info (default) | major | minor | patch'
  )

def execArgs(args):
  config = None
  CurrentVersion = None
  with open('pyproject.toml','r') as infile:
    config = toml.load(infile)
    release = semver.VersionInfo.parse(config['project']['version'])
    CurrentVersion = release
    if args.mode == 'major':
      release = release.replace(major = release.major + 1)
      release = release.replace(minor = 0)
      release = release.replace(patch = 0)
      config['project']['version'] = str(release)   
    elif args.mode == 'minor':
      release = release.replace(minor = release.minor + 1)
      release = release.replace(patch = 0)
      config['project']['version'] = str(release)   
    elif args.mode == 'patch':
      config['project']['version'] = str(release.replace(patch = release.patch + 1))
    else: 
      match = re.match(r'(\d+)\.(\d+)\.(\d+)', args.mode)
      if match:
        release = semver.VersionInfo.parse(args.mode)
        config['project']['version'] = str(release)   

    print (f"version: {config['project']['version']}")

  # save .toml file
  if CurrentVersion != config['project']['version']:
    with open('pyproject.toml','w') as outfile:
      toml.dump(config, outfile)
