# Copyright 2021 The Magenta Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for audio_io.py."""

import io
import os
import wave

from absl.testing import absltest
from note_seq import audio_io
from note_seq import testing_lib
import numpy as np
import scipy


class AudioIoTest(absltest.TestCase):

  def setUp(self):
    super().setUp()
    self.wav_filename = os.path.join(
        testing_lib.get_testdata_dir(), 'example.wav')
    self.wav_filename_mono = os.path.join(
        testing_lib.get_testdata_dir(), 'example_mono.wav')
    self.wav_data = open(self.wav_filename, 'rb').read()
    self.wav_data_mono = open(self.wav_filename_mono, 'rb').read()

  def testWavDataToSamples(self):
    w = wave.open(self.wav_filename, 'rb')
    w_mono = wave.open(self.wav_filename_mono, 'rb')

    # Check content size.
    y = audio_io.wav_data_to_samples(self.wav_data, sample_rate=16000)
    y_mono = audio_io.wav_data_to_samples(self.wav_data_mono, sample_rate=22050)
    self.assertEqual(
        round(16000.0 * w.getnframes() / w.getframerate()), y.shape[0])
    self.assertEqual(
        round(22050.0 * w_mono.getnframes() / w_mono.getframerate()),
        y_mono.shape[0])

    # Check a few obvious failure modes.
    self.assertLess(0.01, y.std())
    self.assertLess(0.01, y_mono.std())
    self.assertGreater(-0.1, y.min())
    self.assertGreater(-0.1, y_mono.min())
    self.assertLess(0.1, y.max())
    self.assertLess(0.1, y_mono.max())

  def testFloatWavDataToSamples(self):
    y = audio_io.wav_data_to_samples(self.wav_data, sample_rate=16000)
    wav_io = io.BytesIO()
    scipy.io.wavfile.write(wav_io, 16000, y)
    y_from_float = audio_io.wav_data_to_samples(
        wav_io.getvalue(), sample_rate=16000)
    np.testing.assert_array_equal(y, y_from_float)

  def testWavDataToSamplesPydub(self):
    w = wave.open(self.wav_filename, 'rb')
    w_mono = wave.open(self.wav_filename_mono, 'rb')

    # Check content size.
    y = audio_io.wav_data_to_samples_pydub(
        self.wav_data, sample_rate=16000, num_channels=1)
    y_mono = audio_io.wav_data_to_samples_pydub(
        self.wav_data_mono, sample_rate=22050, num_channels=1)
    self.assertEqual(
        round(16000.0 * w.getnframes() / w.getframerate()), y.shape[0])
    self.assertEqual(
        round(22050.0 * w_mono.getnframes() / w_mono.getframerate()),
        y_mono.shape[0])

    # Check a few obvious failure modes.
    self.assertLess(0.01, y.std())
    self.assertLess(0.01, y_mono.std())
    self.assertGreater(-0.1, y.min())
    self.assertGreater(-0.1, y_mono.min())
    self.assertLess(0.1, y.max())
    self.assertLess(0.1, y_mono.max())

  def testRepeatSamplesToDuration(self):
    samples = np.arange(5)
    repeated = audio_io.repeat_samples_to_duration(
        samples, sample_rate=5, duration=1.8)
    expected_samples = [0, 1, 2, 3, 4, 0, 1, 2, 3]
    np.testing.assert_array_equal(expected_samples, repeated)


if __name__ == '__main__':
  absltest.main()
