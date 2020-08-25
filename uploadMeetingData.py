from getToken import generateToken
from get_all_meetings import get_meetings
from uploadToCloudStorage import upload_blob
from appendTable import appendBigQueryTable
import http.client
import json
import time
import datetime as dt
import ssl

bucket_name = "{ENTER_BUCKET_NAME}"
source_file_name = "{ENTER_FILE_PATH}"
destination_blob_name = "{ENTER_GCS_BLOB}"
dataset = "{ENTER_DATASET_NAME}"
table = "{ENTER_TABLE_NAME}"
uri = "{ENTER_URI_NAME}"



ssl._create_default_https_context = ssl._create_unverified_context
today = dt.datetime.strftime(dt.datetime.utcnow(),'%Y-%m-%d')
conn = http.client.HTTPSConnection("api.zoom.us")


# Get jwt token for import
token = generateToken()

# Outputs list_of_all_users.txt and list_of_all_users.json
get_meetings(token)

# Upload to Cloud storage
upload_blob(bucket_name, source_file_name, destination_blob_name)

# Upload bucket to BigQuery
appendBigQueryTable(dataset,table,uri)
