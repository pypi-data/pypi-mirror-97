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

"""Tests for drums_encoder_decoder."""

from absl.testing import absltest
from note_seq import drums_encoder_decoder


DRUMS = lambda *args: frozenset(args)
NO_DRUMS = frozenset()


def _index_to_binary(index):
  fmt = '%%0%dd' % len(drums_encoder_decoder.DEFAULT_DRUM_TYPE_PITCHES)
  return fmt % int(bin(index)[2:])


class MultiDrumOneHotEncodingTest(absltest.TestCase):

  def setUp(self):
    self.enc = drums_encoder_decoder.MultiDrumOneHotEncoding()

  def testEncode(self):
    # No drums should encode to zero.
    index = self.enc.encode_event(NO_DRUMS)
    self.assertEqual(0, index)

    # Single drum should encode to single bit active, different for different
    # drum types.
    index1 = self.enc.encode_event(DRUMS(35))
    index2 = self.enc.encode_event(DRUMS(44))
    self.assertEqual(1, _index_to_binary(index1).count('1'))
    self.assertEqual(1, _index_to_binary(index2).count('1'))
    self.assertNotEqual(index1, index2)

    # Multiple drums should encode to multiple bits active, one for each drum
    # type.
    index = self.enc.encode_event(DRUMS(40, 44))
    self.assertEqual(2, _index_to_binary(index).count('1'))
    index = self.enc.encode_event(DRUMS(35, 51, 59))
    self.assertEqual(2, _index_to_binary(index).count('1'))

  def testDecode(self):
    # Zero should decode to no drums.
    event = self.enc.decode_event(0)
    self.assertEqual(NO_DRUMS, event)

    # Single bit active should encode to single drum, different for different
    # bits.
    event1 = self.enc.decode_event(1)
    event2 = self.enc.decode_event(
        2 ** (len(drums_encoder_decoder.DEFAULT_DRUM_TYPE_PITCHES) // 2))
    self.assertEqual(frozenset, type(event1))
    self.assertEqual(frozenset, type(event2))
    self.assertLen(event1, 1)
    self.assertLen(event2, 1)
    self.assertNotEqual(event1, event2)

    # Multiple bits active should encode to multiple drums.
    event = self.enc.decode_event(7)
    self.assertEqual(frozenset, type(event))
    self.assertLen(event, 3)


if __name__ == '__main__':
  absltest.main()
