import http.client
import json
import time
from datetime import datetime, timedelta
import ssl

def get_meetings(token):

    ssl._create_default_https_context = ssl._create_unverified_context
    start = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
    end = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer %s" % token,
        'content-type': "application/json"
        }
    params = "page_size=300&to="+end+"&from="+start+"&type=past"
    conn.request("GET", "/v2/metrics/meetings?"+params, headers=headers)

    res = conn.getresponse()
    print(res)
    data = res.read()

    master_meetings_list = []

    all_meetings = json.loads(data.decode("utf-8"))

    next_page = all_meetings['next_page_token']

    all_meetings = json.loads(data.decode("utf-8"))
    for j in all_meetings['meetings']:
    	master_meetings_list.append(j)

    page_count = all_meetings['page_count']

    while next_page != "":
    	c = 0
    	print(len(master_meetings_list))
    	print('SLEEPING')
    	time.sleep(15)
    	conn.request("GET", "/v2/metrics/meetings?next_page_token="+next_page+"&"+params, headers=headers)

    	res = conn.getresponse()

    	data = res.read()

    	all_meetings = json.loads(data.decode("utf-8"))

    	for j in all_meetings['meetings']:
    		c+=1
    		master_meetings_list.append(j)
    	next_page = all_meetings['next_page_token']
    	print(c)



    #print(len(master_meetings_list))
    with open('list_of_meetings.txt', 'w') as outfile:
        json.dump(master_meetings_list, outfile)


    with open('list_of_meetings.jsonl', 'w') as outfile:
        for entry in master_meetings_list:
            json.dump(entry, outfile)
            outfile.write('\n')
