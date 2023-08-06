import logging
import tempfile

from oauth2client.client import GoogleCredentials

from googleapiclient import errors
from google.api_core import retry
from googleapiclient import discovery

import arguments_definition
import constants
import utils
import gcs_utils
import string_utils
import notebook_utils
from caip_job_executor import CaipJobExecutor

def execute():
  args = arguments_definition.parse_args()

  project_id = args.project_id

  # Get bucket name
  bucket_name = args.bucket_name
  if bucket_name is None:
    bucket_name = "{}-{}".format(project_id, constants.DEFAULT_BUCKET_NAME_SUFFIX)

  # Get current timestamp
  timestamp_str = string_utils.str_time_stamp()

  # Get region
  region = args.region
  if region is None:
    region = constants.DEFAULT_REGION

  # Do we need to download or upload the notebook to GCS?
  input_nb_gcs_path_specified = utils.is_gcs_uri(args.input_notebook)
  output_nb_gcs_path_specified = utils.is_gcs_uri(args.output_notebook)

  # Get input and output notebooks names
  input_notebook_name = utils.get_notebook_name(args.input_notebook)
  output_notebook_name = utils.get_notebook_name(args.output_notebook)

  # Get input notebook URI at GCS
  if input_nb_gcs_path_specified:
    input_notebook_uri = args.input_notebook
  else:
    input_gcs_file_path = utils.get_notebook_gcs_path(input_notebook_name, timestamp_str)
    input_notebook_uri = utils.get_gcs_uri(bucket_name, input_gcs_file_path)

  # Get output notebook URI at GCS
  if output_nb_gcs_path_specified:
    output_notebook_uri = args.output_notebook
  else:
    output_gcs_file_path = utils.get_notebook_gcs_path(output_notebook_name, timestamp_str)
    output_notebook_uri = utils.get_gcs_uri(bucket_name, output_gcs_file_path)

  # Download notebook from GCS if needed
  input_nb_local_file_path = args.input_notebook
  if input_nb_gcs_path_specified:
    tmp_file = tempfile.NamedTemporaryFile()
    input_nb_local_file_path = tmp_file.name

    bucket_name, bucket_path = gcs_utils.get_bucket_name_and_path(args.input_notebook)

    gcs_utils.download(input_nb_local_file_path, project_id, bucket_name, bucket_path)

  # Get image URI
  image_uri = args.container_uri
  if image_uri is None:
    image_uri = notebook_utils.get_container_uri(input_nb_local_file_path)

  if not tmp_file is None:
    tmp_file.close()

  if image_uri is None:
    print("Provided notebook does not have information about its environment. Please specify DL container explicitely using --container-uri parameter.")
    return

  # Get training job ID
  job_id = args.job_id
  if job_id is None:
    job_id = utils.get_job_id(input_notebook_name, timestamp_str)

  # Upload the notebook to GCS if needed
  if not input_nb_gcs_path_specified:
    gcs_utils.check_or_create_bucket(project_id, bucket_name)
    gcs_utils.upload(args.input_notebook, project_id, bucket_name, input_gcs_file_path)

  # Build a representation of the Cloud ML API.
  cloudml = discovery.build('ml', 'v1')
  caip_job_executor = CaipJobExecutor(cloudml.projects().jobs(), project_id, job_id)

  # Get Max running time
  max_running_time = args.max_running_time
  if max_running_time is None:
    max_running_time = constants.DEFAULT_JOB_MAX_RUNNING_TIME_IN_SECONDS

  # Run CAIP training
  try:
    caip_job_executor.submit_training_job(image_uri, region, input_notebook_uri,
                        output_notebook_uri, args.accelerator_type, max_running_time)
  except errors.HttpError as err:
    logging.error('There was an error while running the training job.')
    logging.error(err._get_reason())
    return

  # Download the output notebook if needed
  if not output_nb_gcs_path_specified:
    print('Waiting for Job with ID {} to complete...'.format(job_id))
    caip_job_executor.wait_for_job_completion()
    gcs_utils.download(args.output_notebook, project_id, bucket_name, output_gcs_file_path)

  print("")
  print("Done")