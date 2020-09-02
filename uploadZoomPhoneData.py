from getToken import generateToken
from zoom_phone import get_all_phone_numbers
from uploadToCloudStorage import upload_blob
from overwriteTable import overwriteBigQueryTable
import http.client
import json
import time
import datetime as dt
import ssl

def uploadZoomPhoneData():

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
    get_all_phone_numbers(token)

    # Upload to Cloud storage
    upload_blob(bucket_name, source_file_name, destination_blob_name)

    # Upload bucket to BigQuery
    overwriteBigQueryTable(dataset,table,uri)

uploadZoomPhoneData()
