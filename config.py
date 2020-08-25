"""Google Cloud Storage Configuration."""
from os import environ


# Google Cloud Storage
bucketName = environ.get('{ENTER_BUCKET_NAME}')
bucketFolder = environ.get('{ENTER_GCP_BUCKET_FOLDER_NAME}')
fileToUpload = "{PATH_TO_FOLDER}"
