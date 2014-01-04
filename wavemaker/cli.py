# vim:set ts=8 sw=2 sts=2 et:

"""A command line interface for the wavemaker module."""

import argparse

import wavemaker
from wavemaker import signals


def parse_command_line_arguments():
  """Parse command line arguments.

  Returns:
    An argparse.Namespace object
  """

  parser = argparse.ArgumentParser(
      description='Generate WAVE files.',
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument(
      'output_path',
      help='The path to the resulting WAVE file')

  parser.add_argument(
      '--waveform',
      choices=signals.SignalFactory.WAVEFORMS, default='sine',
      help='The shape of the signal being generated')

  parser.add_argument(
      '--frequency',
      type=float, default=440.0,
      help='The oscillating rate of the wave. A non-negative float, in Hz')

  parser.add_argument(
      '--amplitude',
      type=float, default=1.0,
      help='The amplitude of the wave. A float between 0.0 and 1.0')

  parser.add_argument(
      '--duration',
      type=float, default=1.0,
      help='The time duration of the signal. A non-negative float, in seconds')

  parser.add_argument(
      '--sample_rate',
      type=int, default=44100,
      help='The number of samples per second. A non-negative int, in Hz')

  parser.add_argument(
      '--sample_size',
      type=int, choices=[16], default=16,
      help='The number of bits used to store each sample')

  return parser.parse_args()


def main():
  """The command line entry point for wavemaker."""

  args = parse_command_line_arguments()

  wavemaker.write_wave_file(args.output_path, args.waveform, args.frequency,
                            args.amplitude, args.duration, args.sample_rate,
                            args.sample_size)
