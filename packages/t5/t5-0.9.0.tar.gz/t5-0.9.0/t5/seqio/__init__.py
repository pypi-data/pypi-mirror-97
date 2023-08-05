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

"""Import data modules."""
# pylint:disable=wildcard-import

__version__ = "0.0.0"

from t5.seqio.dataset_providers import *
import t5.seqio.evaluation
from t5.seqio.evaluation import Evaluator
import t5.seqio.experimental
from t5.seqio.feature_converters import *
import t5.seqio.test_utils
from t5.seqio.utils import *
from t5.seqio.vocabularies import *
