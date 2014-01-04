===============================
wavemaker - Generate WAVE files
===============================

This project lives at `GitHub <http://github.com/serban/wavemaker>`_.


Installation
============

You need Python 3. I don't want to support Python 2 for now. This is a pure
Python package with no other dependencies.

I recommend you install the latest version from
`PyPI <http://pypi.python.org/pypi/wavemaker>`_ with ``pip``::

  pip install wavemaker

The standard distutils installation works too::

  tar xzf wavemaker-*.tar.gz
  cd wavemaker-*
  python setup.py install


Usage
=====

The command line tool is called ``make_wave``. This is how you use it::

  make_wave sine-wave.wav

There is more help built in::

  $ make_wave --help
  usage: make_wave [-h] [--waveform {sine}] [--frequency FREQUENCY]
                  [--amplitude AMPLITUDE] [--duration DURATION]
                  [--sample_rate SAMPLE_RATE] [--sample_size {16}]
                  output_path

  Generate WAVE files.

  positional arguments:
    output_path           The path to the resulting WAVE file

  optional arguments:
    -h, --help            show this help message and exit
    --waveform {sine}     The shape of the signal being generated (default:
                          sine)
    --frequency FREQUENCY
                          The oscillating rate of the wave. A non-negative
                          float, in Hz (default: 440.0)
    --amplitude AMPLITUDE
                          The amplitude of the wave. A float between 0.0 and 1.0
                          (default: 1.0)
    --duration DURATION   The time duration of the signal. A non-negative float,
                          in seconds (default: 1.0)
    --sample_rate SAMPLE_RATE
                          The number of samples per second. A non-negative int,
                          in Hz (default: 44100)
    --sample_size {16}    The number of bits used to store each sample (default:
                          16)


API
===

There is a single public API function call. It takes the same arguments that the
command line tool does as keyword arguments. Please see the docstring for more::

  write_wave_file(output_path, waveform='sine', frequency=440.0, amplitude=1.0,
                  duration=1.0, sample_rate=44100, sample_size=16)

Basic usage::

  import wavemaker
  wavemaker.write_wave_file('sine-wave.wav')
