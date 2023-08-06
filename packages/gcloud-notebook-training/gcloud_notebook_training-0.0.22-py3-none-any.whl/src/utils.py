import re
import constants

# Given full environment name returns environment flavor
# E.g. tf-gpu.1-13.m24 => tf-gpu.1-13
def get_env_flavor_from_full_name(full_name):
    index = full_name.rfind(".")
    return full_name[:index] + ":m43"

def get_notebook_name(full_path):
    index = full_path.rfind("/")
    return full_path[index + 1:]

def get_gcs_uri(bucket, path):
    return "gs://{}/{}".format(bucket, path)

def get_notebook_gcs_path(notebook_name, timestamp_str):
    return "{}/{}".format(notebook_name, timestamp_str)

def is_gcs_uri(path):
    return path.startswith("gs://")

def get_job_id(notebook_name, timestamp_str):
    job_id = "job_{}_{}".format(notebook_name, timestamp_str)
    return re.sub(r'\W+', "_", job_id)
