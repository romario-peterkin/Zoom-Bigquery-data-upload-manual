import http.client
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def get_all_imgroups(token):

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = { 'authorization': "Bearer %s" % token }

    conn.request("GET", "/v2/im/groups", headers=headers)

    res = conn.getresponse()
    data = res.read()

    #all_imgroups = data.decode("utf-8")
    all_imgroups = json.loads(data.decode("utf-8"))
    print(all_imgroups['total_records'])


    with open('list_of_imgroups.txt', 'w') as outfile:
        json.dump(all_imgroups['groups'], outfile)

    with open('list_of_imgroups.jsonl', 'w') as outfile:
        for entry in all_imgroups['groups']:
            json.dump(entry, outfile)
            outfile.write('\n')
