import pytest
from notebook_training.src import notebook_utils

def test_get_container_uri():
    assert 'gcr.io/deeplearning-platform-release/tf-gpu.1-15:m43' \
        == notebook_utils.get_container_uri('tests/test.ipynb')