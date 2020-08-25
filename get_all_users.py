import http.client
import json
import time
import datetime as dt
import ssl


def get_all_users(token):


    ssl._create_default_https_context = ssl._create_unverified_context
    today = dt.datetime.strftime(dt.datetime.utcnow(),'%Y-%m-%d')
    conn = http.client.HTTPSConnection("api.zoom.us")

    headers = {
        'authorization': "Bearer %s" % token ,
        'content-type': "application/json"
        }

    conn.request("GET", "/v2/users?page_number=1&page_size=300&status=active", headers=headers)

    res = conn.getresponse()
    data = res.read()


    all_data = json.loads(data.decode("utf-8"))


    page_count = all_data['page_count']
    master_user_list = all_data['users']

    print(page_count)

    i=2
    while i<page_count+1:
    	time.sleep(1)
    	print('SLEEPING: completed page ' + str(i))

    	conn.request("GET", "/v2/users?page_number="+str(i)+"&page_size=300&status=active", headers=headers)

    	res = conn.getresponse()

    	data = res.read()

    	all_data = json.loads(data.decode("utf-8"))

        #print(all_data['users'])

    	master_user_list += all_data['users']

    	i+=1


    with open('list_of_all_users.txt', 'w') as outfile:
        json.dump(master_user_list, outfile)

    with open('list_of_all_users.jsonl', 'w') as outfile:
        for entry in master_user_list:
            json.dump(entry, outfile)
            outfile.write('\n')
