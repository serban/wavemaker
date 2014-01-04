# vim:set ts=8 sw=2 sts=2 et:

from distutils.core import setup

with open('README.rst') as readme_file:
  readme = readme_file.read()

with open('CHANGES.rst') as changes_file:
  changes = changes_file.read()

setup(
  name='wavemaker',
  version='0.1.0',
  description='Generate WAVE files',
  long_description=readme + '\n\n' + changes,
  author='Serban Giuroiu',
  author_email='giuroiu@gmail.com',
  url='http://github.com/serban/wavemaker',
  license='MIT License',
  packages=['wavemaker'],
  scripts=['make_wave'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
  ],
)
