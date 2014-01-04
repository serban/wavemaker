# vim:set ts=8 sw=2 sts=2 et:

"""Store signals."""

import itertools
import struct
import wave


SAMPLE_SIZE = 16  # In bits


class WaveStream(object):
  """A stream of PCM audio data."""

  def __init__(self, channels, sample_rate, sample_size):
    """Initialize a WaveStream with integer samples.

    Args:
      channels: An iterable of the audio channels in the stream. Each item is
        also an iterable containing the samples of that audio channel. All audio
        channels must have the same number of samples. The samples are signed
        integers that fit in the sample size.
      sample_rate: The number of samples per second in the audio stream, in Hz.
      sample_size: The number of bits used to store each sample. Must be 16.
    """

    self.channels = channels
    self.sample_size = sample_size
    self.sample_rate = sample_rate

    self.num_channels = len(channels)
    self.num_samples = len(channels[0])

    # TODO(serban): It's convenient to use the struct module to encode the
    # samples as 16-bit little endian signed integers. To support other sample
    # sizes, like 20 bits or 24 bits per sample, I would need to use another
    # utility to encode the samples. For now, only 16-bit samples are supported.
    assert sample_size == 16, 'Sorry, only 16-bit samples are supported'

  @classmethod
  def from_floating_point(cls, channels, sample_rate):
    """Initialize a WaveStream with floating point samples.

    Args:
      channels: An iterable of the audio channels in the stream. Each item is
        also an iterable containing the samples of that audio channel. All audio
        channels must have the same number of samples. The samples are floats
        between -1.0 and 1.0.
      sample_rate: The number of samples per second in the audio stream, in Hz.

    Returns:
      A WaveStream
    """

    sample_max = 2**(SAMPLE_SIZE-1) - 1
    int_channels = [
        [int(sample * sample_max) for sample in channel]
        for channel in channels]

    return cls(int_channels, sample_rate, SAMPLE_SIZE)

  def get_interleaved_samples(self):
    """Interleave the samples in the channels into a single bytestring.

    Returns:
      A bytestring of little endian signed integers
    """

    num_interleaved_samples = self.num_channels * self.num_samples
    interleaved_samples = itertools.chain.from_iterable(zip(*self.channels))

    struct_format = '<{}h'.format(num_interleaved_samples)
    return struct.pack(struct_format, *interleaved_samples)

  def write_wave_file(self, output_path):
    """Write a WAVE file of the stream contents.

    Args:
      output_path: The path to the resulting WAVE file.
    """

    # TODO(serban): As of January 2014, Python 3.4 is still in beta. wave.open()
    # supports the context manager protocol in Python 3.4, but I'll wait until
    # it becomes stable before using a context manager here. See
    # http://docs.python.org/dev/whatsnew/3.4.html#wave for more information.
    output_file = wave.open(output_path, 'wb')

    output_file.setsampwidth(self.sample_size // 8)
    output_file.setframerate(self.sample_rate)
    output_file.setnchannels(self.num_channels)
    output_file.setnframes(self.num_samples)
    output_file.setcomptype('NONE', 'not compressed')

    output_file.writeframes(self.get_interleaved_samples())
    output_file.close()
