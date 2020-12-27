import logging, time
import config
from upload_to_s3 import upload_to_s3

upload_to_s3(body="Hi group 3!", filename="group3-test.txt")
