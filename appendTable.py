from google.cloud import bigquery

def appendBigQueryTable(dataset, table, uri):
    client = bigquery.Client()
    table_ref = client.dataset(dataset).table(table)

    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    #uri = "gs://test_zoom_data/list_of_all_users.jsonl"
    load_job = client.load_table_from_uri(
    uri, table_ref, job_config=job_config
    )  # API request
    print("Starting BQ job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(table_ref)
    print("Loaded {} rows.".format(destination_table.num_rows))
