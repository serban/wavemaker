#!/usr/bin/env python
# vim:set ts=8 sw=2 sts=2 et:

# Copyright (c) 2013 Serban Giuroiu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import argparse
import itertools
import math
import struct
import wave


SAMPLE_SIZE = 16  # In bits


class WaveStream:
  def __init__(self, channels, sample_rate):
    self.channels = channels
    self.sample_size = SAMPLE_SIZE
    self.sample_rate = sample_rate

    self.num_channels = len(channels)
    self.num_samples = len(channels[0])

  def get_interleaved_samples(self):
    # TODO(serban): It's convenient to use the struct module to encode the
    # samples as 16-bit little endian signed integers. To support other sample
    # sizes, like 20 bits or 24 bits per sample, I would need to use another
    # utility to encode the samples. For now, only 16-bit samples are supported.
    assert self.sample_size == 16, 'Sorry, only 16-bit samples are supported'

    num_interleaved_samples = self.num_channels * self.num_samples
    interleaved_samples = itertools.chain.from_iterable(zip(*self.channels))

    # Wave file samples are little-endian signed integers
    struct_format = '<{num_interleaved_samples}h'.format(
        num_interleaved_samples=num_interleaved_samples)

    return struct.pack(struct_format, *interleaved_samples)


def make_discrete_sine_wave_signal(frequency, amplitude, length, sample_rate):
  signal = list()

  num_samples = int(length * sample_rate)
  max_sample = 2**(SAMPLE_SIZE-1) - 1

  for i in range(num_samples):
    sample = int((amplitude * max_sample) *
                 math.sin(2 * math.pi * frequency * (i / sample_rate)))
    signal.append(sample)

  return signal


def make_sine_wave_stream(frequency, amplitude, length, sample_rate):
  signal = make_discrete_sine_wave_signal(frequency, amplitude, length,
                                          sample_rate)
  channels = [signal, signal]

  return WaveStream(channels, sample_rate)


def write_wave_stream(wave_stream, output_path):
  # TODO(serban): As of December 2013, Python 3.4 is still in beta. wave.open()
  # supports the context manager protocol in Python 3.4, but I'll wait until it
  # becomes stable before using a context manager here. See
  # http://docs.python.org/dev/whatsnew/3.4.html#wave for more information.
  output_file = wave.open(output_path, 'wb')

  output_file.setsampwidth(wave_stream.sample_size // 8)
  output_file.setframerate(wave_stream.sample_rate)
  output_file.setnchannels(wave_stream.num_channels)
  output_file.setnframes(wave_stream.num_samples)
  output_file.setcomptype('NONE', 'not compressed')

  output_file.writeframes(wave_stream.get_interleaved_samples())
  output_file.close()


def get_command_line_args():
  parser = argparse.ArgumentParser(
      description='Generate a sine wave in a WAVE file.',
      epilog='The output file contains 16-bit samples.')

  parser.add_argument('output_path', help='The path to the resulting Wave file')

  parser.add_argument('--frequency', type=float, default=440.0,
                      help='A non-negative floating point number, in Hz')
  parser.add_argument('--amplitude', type=float, default=1.0,
                      help='An floating point number between 0.0 and 1.0')
  parser.add_argument('--length', type=float, default=1.0,
                      help='A non-negative floating point number, in seconds')
  parser.add_argument('--sample_rate', type=int, default=44100,
                      help='A non-negative integer, in samples per second')

  return vars(parser.parse_args())


def main():
  args = get_command_line_args()

  wave_stream = make_sine_wave_stream(args['frequency'], args['amplitude'],
                                      args['length'], args['sample_rate'])
  write_wave_stream(wave_stream, args['output_path'])


if __name__ == '__main__':
  main()
