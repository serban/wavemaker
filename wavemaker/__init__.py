# vim:set ts=8 sw=2 sts=2 et:

"""Generate WAVE files."""

from wavemaker import signals

def write_wave_file(output_path, waveform='sine', frequency=440.0,
                    amplitude=1.0, duration=1.0, sample_rate=44100,
                    sample_size=16):
  """Generate a WAVE file.

  Args:
    output_path: The path to the resulting WAVE file.
    waveform: The shape of the signal being generated. Must be 'sine'.
    frequency: The oscillating rate of the wave. A non-negative float, in Hz.
    amplitude: The amplitude of the wave. A float between 0.0 and 1.0.
    duration: The time duration of the signal. A non-negative float, in seconds.
    sample_rate: The number of samples per second. A non-negative int, in Hz.
    sample_size: The number of bits used to store each sample. Must be 16.
  """

  wave_stream = signals.SignalFactory.make_signal(
      waveform, frequency, amplitude, duration, sample_rate, sample_size)

  wave_stream.write_wave_file(output_path)
