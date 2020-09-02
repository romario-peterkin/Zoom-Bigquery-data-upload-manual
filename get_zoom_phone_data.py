import http.client
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_all_phone_numbers(token):

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = { 'authorization': "Bearer %s" % token }

    conn.request("GET", "/v2/phone/numbers", headers=headers)

    res = conn.getresponse()
    data = res.read()

    all_phone_numbers = json.loads(data.decode("utf-8"))


    with open('zoom_phone_numbers.txt', 'w') as outfile:
        json.dump(all_phone_numbers['phone_numbers'], outfile)

    with open('zoom_phone_numbers.jsonl', 'w') as outfile:
        for entry in all_phone_numbers['phone_numbers']:
            json.dump(entry, outfile)
            outfile.write('\n')
