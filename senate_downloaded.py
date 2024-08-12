import requests
import time as t
import json

import random as r
import re

def random_user_agent(typ="str"):#requests lib is very picky while selenium isn't 
    agents = open("agents.txt", "r")
    agent = r.choice(agents.readlines())
    agents.close()
    if typ == "dict":
        balls = dict()
        balls["User-Agent"] = str(agent).replace("\n", "")
        return balls

    elif typ == "SEC":
        balls = dict()
        balls["User-Agent"] = "Amazon Inc learning@gmail.com"
        return balls
    else:
        return agent  

def file_request(url, to=5):
    file_str = ''
    headers = random_user_agent("dict")

    try:
        file_str = requests.get(url, headers=headers, timeout=to)

    except requests.exceptions.ConnectionError:
        print("failed to resolve hostname: back in 1")
        t.sleep(60)#changed from 10 to reduce wasted time
        return file_request(url)
    except requests.exceptions.ReadTimeout:
        return file_request(url, 60)

    return file_str.json()

def update_total(total):
	f = open("total.txt", "w+")
	f.write(str(total))
	f.close()


url = "https://lda.senate.gov/api/v1/filings/?page=1&filing_year="
ite = 1
og_start = t.time()
start_of_requests = t.time()

year = 2024
lobbying_file = open("lobbying_data.json", "a+")

try:
	resume = int(open("total.txt", "r").read())
except Exception:
	resume = 0

total_records = 0
temp_total_records = 0
while year > 1998:
    t.sleep(60)
    all_lobbying_data = file_request(url+str(year))
    temp_total_records = 0
    print("starting year: " + str(year))
    
    while("next" in list(all_lobbying_data.keys()) and all_lobbying_data["next"] is not None):#keys?

        if resume != 0 and (resume > total_records and resume-25 > total_records):
            total_records+=25
            temp_total_records+=25
            continue

        if ite%15 == 0:
            if ite%75 == 0 and resume < total_records:print("Time since start: " + str(round((t.time()-og_start)/60, 2)) + "(min)\nfilings processed: "+str(temp_total_records)+" "+str(round(((temp_total_records)/all_lobbying_data["count"])*100, 2))+"%")
            pause_time = 60-round(t.time()-start_of_requests)
            if pause_time > 0:
                t.sleep(pause_time)

        for filing_bit in all_lobbying_data["results"]:
            total_records+=1
            temp_total_records+=1
            if resume < total_records:
                lobbying_file.write(json.dumps(filing_bit)+"\n")

        c = all_lobbying_data["next"]       
        if len(c) <= 4:break
        all_lobbying_data = file_request(all_lobbying_data["next"])
        ite+=1

        try:
            while str(all_lobbying_data).find("Request was throttled. Expected available in") != -1 or str(all_lobbying_data).find("'You must pass at least one query string parameter to filter the results and be able to paginate the results.") != -1:
                t.sleep(60)
                #print("stalling")
                all_lobbying_data = file_request(c)
        except KeyError:
            print("failed")
            continue
        
        update_total(total_records)

    year-=1

print("total total records analyzed: " + str(total_records)+" in:"+str((t.time()-og_start)/60) + " Min")
lobbying_file.close()
