from __future__ import absolute_import
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from .tensors import Tensor

X = Tensor('s', 3, 5)
X.pprint(print_format=2)
