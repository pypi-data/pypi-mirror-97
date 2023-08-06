
DL_PATH = "/opt/deeplearning"
DL_METADATA_PATH = "{}/metadata".format(DL_PATH)
ENV_VERSION_FILE_PATH = "{}/env_version".format(DL_METADATA_PATH)
GCR_URL_TEMPLATE = "gcr.io/deeplearning-platform-release/{}"
DEFAULT_BUCKET_NAME_SUFFIX = "notebook-training"
NOT_FOUND_INDEX = -1
JOB_GET_TIMEOUT_IN_SECONDS = 12 * 60 * 60 # 12 hours
DEFAULT_REGION = "us-central1"
TRAINING_JOB_STATES_TO_WAIT = {
        "QUEUED",
        "PREPARING",
        "RUNNING"
        }
TRAINING_JOB_PREPARATION_TIME_IN_SECONDS = 8 * 60 + 30 # 8.5 minutes
DEFAULT_JOB_MAX_RUNNING_TIME_IN_SECONDS = 9 * 60 * 60 # 9 hours