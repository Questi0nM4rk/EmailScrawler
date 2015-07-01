__author__ = 'John Lorio'

from bs4 import BeautifulSoup
import requests
import requests.exceptions
import time
from collections import deque
import re


def stopwatch(sec):
    time.sleep(1*sec)


# URLs ****
newUrls = deque([])
# Used URLs ****
usedUrls = set()
# Email Addresses ****
eMails = set()
headers = {}
headers["User Agent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                        ' Chrome/43.0.2357.130 Safari/537.36'

ipage = 0


def indeed(pages):
    global ipage
    while ipage != pages:
        ipage += 1

        # jobList = ["it", "specialist", "help desk", "desktop support", "service desk"]
        # jobTitles = []
        url2 = ""
        indLink = "http://www.indeed.com"
        if ipage == 1:
            url2 = "http://www.indeed.com/jobs?q=information+technology&l=San+Antonio%2C+TX"
        elif ipage >= 2:
            url2 = "http://www.indeed.com/jobs?q=information+technology&l=San+Antonio%2C+TX&start=" \
                   + str((ipage * 10) - 10)

        r = requests.get(url2)

        soup = BeautifulSoup(r.content)
        gData = soup.find_all("a", {"itemprop": "title"})

        for item in gData:
            # contentsZero = item.contents[0]
            href = item.get("href")

            # jobNum = len(contentsZero)
            # jobTitles.append(contentsZero)
            newAdd = indLink + href
            newUrls.appendleft(newAdd)
            if len(newUrls) % 10 == 0:
                print(str(len(newUrls)) + " New Indeed Urls!")

        if ipage % 5 == 0:
            print(" Indeed Page" + " " + str(ipage))
    print(str(len(newUrls)) + " TOTAL URLS")
    print(str(ipage) + " TOTAL PAGES")


def simplyHired(pages):
    global ipage

    while ipage != 10:

            ipage += 1

            url2 = ""
            shLink = "http://www.simplyhired.com"

            if ipage == 1:
                url2 = "http://www.simplyhired.com/search?q=information+technology&l=San+Antonio%2C+TX"
            elif ipage >= 2:
                url2 = "http://www.simplyhired.com/search?q=information+technology&l=San+Antonio%2C+TX&pn=" + str(ipage)

            r = requests.get(url2)
            soup = BeautifulSoup(r.content)
            gData = soup.find_all("a", {"class": "title"})

            for i in gData:
                href = i.get("href")

                newAdd = shLink + href
                newUrls.appendleft(newAdd)
            if len(newUrls) % 10 == 0:
                print(str(len(newUrls)) + " New Simply Hired Urls!")

    if ipage % 5 == 0:
            print(" Monster Page" + " " + str(ipage))
    print(str(len(newUrls)) + " TOTAL URLS")
    print(str(ipage) + " TOTAL PAGES")


def mailScraper():
    urlCount = 0
    while len(newUrls) != 0:
        url = newUrls.popleft()
        usedUrls.add(url)
        urlCount += 1

        print("Processing %s" % url + " NO." + str(urlCount))
        try:
            response = requests.get(url)

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # Ignore ****
            continue

        # Extract All Emails and add them to set ****
        newEmails = set(re.findall(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}', response.text, re.I))

        eMails.update(newEmails)

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content)

        try:
            response = soup.get_text()

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue
        newEmails = set(re.findall(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}', response, re.I))

        eMails.update(newEmails)
    for ele in eMails:
        print(ele.upper())
    print(len(eMails))
    print(str(len(usedUrls)) + " Used Urls.")
    print(str(len(newUrls)) + " New Urls.")



simplyHired(10)

mailScraper()





