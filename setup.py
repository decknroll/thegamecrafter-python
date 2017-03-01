from distutils.core import setup
setup(
  name = 'thegamecrafter',
  packages = ['thegamecrafter'], # this must be the same as the name above
  version = '0.9.1',
  description = 'A Python abstraction layer around the TheGameCrafter API.',
  author = 'Clarence "Sparr" Risher, Neil Durbin, John Coogan, Clark Fischer',
  author_email = 'sparr0@gmail.com',
  url = 'https://github.com/sparr/thegamecrafter-python', # use the URL to the github repo
  download_url = 'https://github.com/sparr/thegamecrafter-python/archive/master.tar.gz', # I'll explain this in a second
  keywords = ['thegamecrafter', 'api', 'wrapper', 'sparr'], # arbitrary keywords
  classifiers = [],
  install_requires = ['requests >= 2.4.3'],
)
