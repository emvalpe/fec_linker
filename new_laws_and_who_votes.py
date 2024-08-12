import requests
import time as t
import json

import random as r
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.actions import ActionChains


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
        print("failed to resolve hostname: back in 10")
        t.sleep(600)
        return file_request(url)
    except requests.exceptions.ReadTimeout:
        return file_request(url, 60)

    return file_str.text


def dump_bs(url):
    file = file_request(url)
    bs = BeautifulSoup(file, "lxml")

    return bs

"""
congress: 
- add dig deeper 
- test
- compare vote a????

bill info:
- check if already written

house of reps votes:
- add dig deeper
- test

"""
def legislation_passed():
    rss_feeds = ['https://www.govinfo.gov/rss/hob.xml','https://www.govinfo.gov/rss/comps-bulkdata.xml [what exactly is this]','https://www.govinfo.gov/rss/billsum-bulkdata.xml','https://www.govinfo.gov/rss/bills.xml']
    for rss_feed in rss_feeds:
        feed = dump_bs(file_request(rss_feed))
        fil = open(rss_feed[rss_feed.rfind("/"):], "w+")
        for item in feed.find_all("item"):
            fil.write(str(item))

        fil.close()

def house_voters():
    link = "https://clerk.house.gov/Votes"
    f = open("house_votes.json", "w+")

    driver = webdriver.Firefox()
    driver.get(url)
    start = driver.find_element(By.ID, "membersvotes")
    ite = 0
    page_mover = start.find_element(By.TAG_NAME, "nav")
    v = int(page_mover.find_element(By.CLASS_NAME, "pagination_info").text[10:14])

    while ite < v:
        page_mover = start.find_element(By.TAG_NAME, "nav")
        nxt = page_mover.find_element(By.TAG_NAME, "ul").find_all(By.TAG_NAME, "li")[-1].find_element(By.TAG_NAME, "a")
        #.click above when done to go to next

        for i in start.find_element(By.ID, "votes").find_all(By.TAG_NAME, "div"):
            elems = i.find_all(By.TAG_NAME, "div")
            dig_deeper = i[1] #add to get itemized votes for/against bills

            vote = {}
            divs = elems[0].find_all(By.TAG_NAME, "div")

            frow = divs[0].find_element(By.CLASS_NAME, "first-row").text
            vote["date"] = frow[:frow.find("|")]
            vote["congress session"] = frow[frow.find("|"):]

            heading = divs[0].find_element(By.CLASS_NAME, "heading").find_all(By.TAG_NAME, "a")
            vote["members present"] = heading[0].text
            vote["bill"] = heading[1].text

            ps = divs[0].find_all(By.TAG_NAME, "p")
            vote["purpose of vote"] = p[0].text
            vote["bill description"] = p[1].find_element(By.CLASS_NAME, "billdesc").text
            vote["vote type"] = p[2].text
            vote["vote result"] = p[3].text

            caps = divs[1].find_all(By.CLASS_NAME, "capitalize")
            vote["vote in support"] = caps[0].find_element(By.TAG_NAME, "p").text
            vote["vote against"] = caps[1].find_element(By.TAG_NAME, "p").text
            vote["congress people physically present"] = caps[2].find_element(By.TAG_NAME, "p").text
            vote["not voting"] = caps[3].find_element(By.TAG_NAME, "p").text
            f.write(str(vote))
            ite+=1

        nxt.click()

    f.close()

def senate_voters():
    link = "https://www.govtrack.us/congress/votes#chamber[]=1&session=__ALL__"

    f = open("congress_votes.json", "w+")

    driver = webdriver.Chromium()
    driver.get(url)

    start = driver.find_element(By.CLASS_NAME, "searching")
    total = start.find_element(By.CLASS_NAME, "order-md-1").find_element(By.CLASS_NAME, "total").text
    results = start.find_element(By.CLASS_NAME, "results")

    count = 0
    while count < total:
        for i in results.find_all(By.TAG_NAME, "div"):
            if i.CLASS_NAME != "row" or i.CLASS_NAME != "":continue

            vote = {}

            count += 1
            if count == 1:
                data = i.find_element(By.CLASS_NAME, "row").find_element("col-xs-10")
            
            else:
                data = i.find_element("col-xs-10")

            div = data.find_element(By.TAG_NAME, "div")
            dig_deeper = div[0].find_element(By.TAG_NAME, "a")
            vote["subject of vote"] = dig_deeper.text

            surface_data = div[1].find_all(By.TAG_NAME, "div")#dont read 3rd
            e = surface_data[0].find_all(By.TAG_NAME, "div")
            vote["vote number"] = e[0].text
            vote["date"] = e[1].text

            res = surface_data.find_element(By.TAG_NAME, "div").text.split(" ")
            vote["result"] = res[:-1]
            vote["votes in favor"] = res[-1][:res.find("/")]
            vote["votes against"] = res[-1][res.find("/"):]

        ActionChains(driver).scroll_to_element(driver.find_element(By.ID, "footer")).perform()
        t.sleep(3)
