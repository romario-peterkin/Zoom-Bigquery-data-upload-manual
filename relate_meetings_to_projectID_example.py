import json
import pandas as pd
import datetime as dt
from uploadToCloudStorage import upload_blob
from appendTable import appendBigQueryTable



#Function that takes in IM group name and returns ProjectID
def imgroupid_to_projectid(imgroupid):
	imname = imid_to_imname[imgroupid]
	if imname in groups_to_skip:
		g = 'continue'
	if imname not in imname_to_projectid.keys():
		g = 'continue'
	else:
		g = imname_to_projectid[imname]
	return(g)

#I don't want to include these groups in a meeting list, they were for testing. This is not a complete list.
groups_to_skip = ['C19-Client : Facility ','Zoom Testing','COVID_Test - Capitol Hill'
					,'COVID_Test - Montlake','Hospital A']

#Get today's date
today = dt.datetime.strftime(dt.datetime.utcnow(),'%Y-%m-%d')

#Open up a local file that contains all of our users.
with open('list_of_all_users.txt') as json_file:
	all_users = json.load(json_file)

#Build a dictionary that has user emails as keys and a list of all their IM groups as values
users_to_imgroups = {}
for i in all_users:
     if 'im_group_ids' in i.keys():
             users_to_imgroups[i['email']] = i['im_group_ids']

#Load a local file that relates project ID to IM group names. Create a dictionary that has IM group name as key and projectID as value
ID_to_IM = pd.read_csv("project_ID_to_imgroup.csv")
imname_to_projectid = dict(zip(ID_to_IM['IM Group'],ID_to_IM['Project ID']))

#Load a local file that has all meetings in Zoom
with open('list_of_meetings.txt') as json_file:
	all_meetings = json.load(json_file)

#Load a local file that contains all IM groups that exist in Zoom
with open('list_of_imgroups.txt') as json_file:
	all_imgroups = json.load(json_file)

#Build a dictionary that relates IMgroup ID to the IM group name
imid_to_imname = {}
for j in all_imgroups:
     imid_to_imname[j['id']] = j['name']

c=0
all_meetings_projectid = []
#Go through all meetings in the list
for meeting in all_meetings:

	#Check if the host is in a IM group
	if meeting['email'] in users_to_imgroups.keys():
		groups = users_to_imgroups[meeting['email']]

		#Handle specifically if the user is in only one IM groups
		if len(groups)<2:
			groups = groups[0]
			groups = imgroupid_to_projectid(groups)
			if groups == 'continue':
				continue

			meeting['projectIDs'] = groups
			c+=1

		#Handle specifically if the user is in multiple IM groups. Project IDs get delimted with semicolumns.
		else:
			group_str = ""
			for sr in groups:
				s = str(imgroupid_to_projectid(sr))

				if len(group_str) <1:
					group_str = s
					group_str = "'" + str(group_str) + "'"
				else:
					group_str = group_str+";"+s

			if 'continue' not in group_str:
				meeting['projectIDs'] = group_str
				c+=1
		all_meetings_projectid.append(meeting)

with open('list_of_meetings_project_id.jsonl', 'w') as outfile:
    for entry in all_meetings_projectid:
        json.dump(entry, outfile)
        outfile.write('\n')

# Formatting


master_list = []


with open('list_of_meetings_project_id.jsonl','r') as f:
    data = json.loads("[" +
        f.read().replace("}\n{", "},\n{") +
    "]")

    for i in data:
        try:
            if type(i['projectIDs']) is int:
                #print(str(i['projectIDs']))
                i['projectIDs'] = str(i['projectIDs'])
                #print(i)
                master_list.append(i)
                data.pop(i)
            else:
                master_list.append(i)



        except:
            x=0



    with open('list_of_meetings_project_id(F).jsonl', 'w') as outfile:
        json.dump(master_list, outfile)


    with open('list_of_meetings_project_id(F).jsonl', 'r') as my_file:
        text = my_file.read()
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("},", "}\n")


    with open('list_of_meetings_project_id(F).jsonl', 'w') as my_file:
        my_file.write(text)


    bucket_name = "zoom-data"
    source_file_name = "/Users/romario.peterkin/Desktop/BQ/list_of_meetings_project_id(f).jsonl"
    destination_blob_name = "list_of_meetings_project_id.jsonl"
    dataset = 'zoom'
    table = 'list_of_meetings_project_id'
    uri = "gs://zoom-data/list_of_meetings_project_id.jsonl"





    # Upload to Cloud storage
    upload_blob(bucket_name, source_file_name, destination_blob_name)

    # Upload bucket to BigQuery
    appendBigQueryTable(dataset,table,uri)
