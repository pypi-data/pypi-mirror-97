# Copyright 2021 The T5 Authors.
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

"""Tests for seqio.preprocessors."""

from absl.testing import absltest
from t5.seqio import dataset_providers
from t5.seqio import preprocessors
from t5.seqio import test_utils
import tensorflow.compat.v2 as tf

assert_dataset = test_utils.assert_dataset
Feature = dataset_providers.Feature


class PreprocessorsTest(absltest.TestCase):

  def test_tokenize(self):
    og_dataset = tf.data.Dataset.from_tensors({
        'prefix': 'This is',
        'suffix': 'a test.'
    })
    output_features = {
        'prefix': Feature(
            test_utils.MockVocabulary({'This is': [0, 1]}), add_eos=True),
        'suffix': Feature(
            test_utils.MockVocabulary({'a test.': [2, 3]}), add_eos=False),
    }

    assert_dataset(
        preprocessors.tokenize(og_dataset, output_features=output_features), {
            'prefix': [0, 1],
            'prefix_pretokenized': 'This is',
            'suffix': [2, 3],
            'suffix_pretokenized': 'a test.'
        })
    assert_dataset(
        preprocessors.tokenize(
            og_dataset, output_features=output_features,
            copy_pretokenized=False),
        {
            'prefix': [0, 1],
            'suffix': [2, 3]
        })

    assert_dataset(
        preprocessors.tokenize_and_append_eos(
            og_dataset, output_features=output_features,
            copy_pretokenized=False),
        {
            'prefix': [0, 1, 1],
            'suffix': [2, 3]
        })

  def test_append_eos(self):
    og_dataset = tf.data.Dataset.from_tensors({
        'inputs': [1, 2, 3],
        'targets': [4, 5, 6, 7],
        'arrows': [8, 9, 10, 11],
        'bows': [12, 13],
    })
    vocab = test_utils.sentencepiece_vocab()
    output_features = {
        'inputs': Feature(vocab, add_eos=False),
        'targets': Feature(vocab, add_eos=True),
        'arrows': Feature(vocab, add_eos=True),
    }
    sequence_length = {
        'inputs': 4,
        'targets': 3,
        'arrows': 5,
        'bows': 1
    }

    # Add eos only.
    assert_dataset(
        preprocessors.append_eos(og_dataset, output_features),
        {
            'inputs': [1, 2, 3],
            'targets': [4, 5, 6, 7, 1],
            'arrows': [8, 9, 10, 11, 1],
            'bows': [12, 13],
        })

    # Trim to sequence lengths.
    assert_dataset(
        preprocessors.append_eos_after_trim(
            og_dataset,
            output_features=output_features,
            sequence_length=sequence_length),
        {
            'inputs': [1, 2, 3],
            'targets': [4, 5, 1],
            'arrows': [8, 9, 10, 11, 1],
            'bows': [12, 13],
        })

    # Don't trim to sequence lengths.
    assert_dataset(
        preprocessors.append_eos_after_trim(
            og_dataset,
            output_features=output_features),
        {
            'inputs': [1, 2, 3],
            'targets': [4, 5, 6, 7, 1],
            'arrows': [8, 9, 10, 11, 1],
            'bows': [12, 13],
        })


if __name__ == '__main__':
  absltest.main()
