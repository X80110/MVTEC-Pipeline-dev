# REPLACE THIS WITH YOUR NAME without spaces i.e. "mosborn"
# this will set the target upload folder on S3 to your own directory
folder="project"

bucket="mvtec-group3"
region="eu-west-1"

# some logging config
import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if folder=="TEST":
    logging.warn("\n\nPlease set your `folder` variable in the config.py. Read the README for more information.\n\n")
