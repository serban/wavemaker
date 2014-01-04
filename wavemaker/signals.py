# vim:set ts=8 sw=2 sts=2 et:

"""Generate signals."""

import math

from wavemaker import wave_stream


class InvalidWaveformError(Exception):
  """Raised when attempting to use an invalid waveform."""


def make_sine_wave_signal(frequency, amplitude, duration, sample_rate):
  """Generate a sine wave signal.

  Args:
    frequency: The oscillating rate of the wave. A non-negative float, in Hz.
    amplitude: The amplitude of the wave. A float between 0.0 and 1.0.
    duration: The time duration of the signal. A non-negative float, in seconds.
    sample_rate: The number of samples per second. A non-negative int, in Hz.

  Returns:
    A WaveStream representing the signal
  """

  signal = list()
  num_samples = int(duration * sample_rate)

  for i in range(num_samples):
    sample = amplitude * math.sin(2 * math.pi * frequency * (i / sample_rate))
    signal.append(sample)

  channels = [signal, signal]

  return wave_stream.WaveStream.from_floating_point(channels, sample_rate)


class SignalFactory(object):
  """Make signals."""

  WAVEFORMS = ['sine']

  # pylint: disable=unused-argument
  @classmethod
  def make_signal(cls, waveform='sine', frequency=440.0, amplitude=1.0,
                  duration=1.0, sample_rate=44100, sample_size=16):
    """Generate a signal with a particular waveform.

    Args:
      waveform: The shape of the signal being generated. Must be in WAVEFORMS.
      frequency: The oscillating rate of the wave. A non-negative float, in Hz.
      amplitude: The amplitude of the wave. A float between 0.0 and 1.0.
      duration: The duration of the signal. A non-negative float, in seconds.
      sample_rate: The number of samples per second. A non-negative int, in Hz.
      sample_size: The number of bits used to store each sample. Must be 16.

    Returns:
      A WaveStream representing the signal
    """
    if waveform not in cls.WAVEFORMS:
      raise InvalidWaveformError(
          '|waveform| = {waveform!r} is not a valid waveform. Valid waveforms '
          'are {valid_waveforms!r}.'.format(waveform=waveform,
                                            valid_waveforms=cls.WAVEFORMS))

    if waveform == 'sine':
      return make_sine_wave_signal(frequency, amplitude, duration, sample_rate)
