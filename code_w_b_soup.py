from bs4 import BeautifulSoup
import urllib2
import requests
import pdb

cik = "0001166559"

url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&Find=Search".format(cik)

page = urllib2.urlopen(url)
html = BeautifulSoup(page, "lxml")

list_of_all_13f_links = []

all_td = html.find_all("td")

for element in all_td:
    if "13F" in element.text:
        list_of_all_13f_links.append(element.next_sibling.next_sibling.a.get("href"))

for link in list_of_all_13f_links:
    detail_url = "https://www.sec.gov{}".format(link)
    detail_page = urllib2.urlopen(detail_url)
    detail_html = BeautifulSoup(detail_page, "lxml")
