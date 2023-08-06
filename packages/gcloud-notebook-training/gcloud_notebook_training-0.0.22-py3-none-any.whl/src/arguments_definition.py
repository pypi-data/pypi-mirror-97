import argparse

def parse_args():
  parser = argparse.ArgumentParser(
        description="Get notebook training args")

  parser.add_argument("--project-id", required=True)
  parser.add_argument("--input-notebook", required=True)
  parser.add_argument("--output-notebook", required=True)
  parser.add_argument("--job-id", required=False)
  parser.add_argument("--region", required=False)
  parser.add_argument("--worker-machine-type", required=False)
  parser.add_argument("--bucket-name", required=False)
  parser.add_argument("--max-running-time", required=False)
  parser.add_argument("--container-uri", required=False)
  parser.add_argument("--accelerator-type", required=False)

  args = parser.parse_args()
  return args