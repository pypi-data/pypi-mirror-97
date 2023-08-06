"""
Fixtures
--------
"""

import pytest
import numpy as np
from sentence_transformers import (
    SentenceTransformer,
)  # required or the import within wikirec.visuals will fail

import wikirec

from wikirec import data_utils
from wikirec import model
from wikirec import utils

np.random.seed(42)


@pytest.fixture(params=[])
def fixture(request):
    return request.param
