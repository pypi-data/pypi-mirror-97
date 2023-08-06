import pytest
from notebook_training.src import utils

def test_get_notebook_name_absolute():
    assert 'notebook.ipynb' == utils.get_notebook_name('/some/path/for/notebook.ipynb')

def test_get_notebook_name_local():
    assert 'notebook.ipynb' == utils.get_notebook_name('notebook.ipynb')

def test_get_notebook_name_gcs():
    assert 'notebook.ipynb' == utils.get_notebook_name('gs://bucket_name/path/to/notebook.ipynb')

def test_is_gcs_uri_true():
    assert utils.is_gcs_uri("gs://gcs/path")

def test_is_gcs_uri_false():
    assert not utils.is_gcs_uri("/local/path")

def test_get_job_id():
    assert "Notebook_ipynb_2019_23_05_12_34_4535_34545" \
        == utils.get_job_id("Notebook.ipynb", "2019/23/05-12:34:4535.34545")