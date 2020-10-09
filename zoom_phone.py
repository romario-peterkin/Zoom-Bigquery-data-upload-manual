import http.client
import json
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

def get_all_phone_numbers(token):

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = { 'authorization': "Bearer %s" % token }

    conn.request("GET", "/v2/phone/numbers", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #all_phone_numbers = data.decode("utf-8")
    all_phone_numbers = json.loads(data.decode("utf-8"))
    print(all_phone_numbers['total_records'])


    with open('zoom_phone_numbers.jsonl', 'w') as outfile:
        for entry in all_phone_numbers['phone_numbers']:
            json.dump(entry, outfile)
            outfile.write('\n')



    print("List of Zoom Phone numbers compiled to zoom_phone_numbers.jsonl")
