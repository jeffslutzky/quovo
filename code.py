from bs4 import BeautifulSoup, NavigableString
import urllib2
import pdb
import csv
import sys
from xmlutils.xml2csv import xml2csv

# cik = raw_input("Enter a ticker or symbol: ")

cik = "0001166559"

url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&Find=Search".format(cik)

page = urllib2.urlopen(url)
html = BeautifulSoup(page, "lxml")
list_of_all_13f_links = []
list_of_txt_urls_to_parse = []
all_td = html.find_all("td")

def get_details(link):
    detail_url = "https://www.sec.gov{}".format(link)
    detail_page = urllib2.urlopen(detail_url)
    detail_html = BeautifulSoup(detail_page, "lxml")
    for anchor in detail_html.find_all("a"):
        url = "https://www.sec.gov{}".format(anchor.get("href"))
        if ".txt" in url:
            list_of_txt_urls_to_parse.append(url)

def get_raw_data(tag, data):
    cols = []
    d = {}
    for child in tag:
        if hasattr(child, "name") and not isinstance(child, NavigableString):
            if not child.find_all(True): # if there's no deeper child:
                keyname = child.parent.name + ":" + child.name
                if child.parent.parent:
                    keyname = child.parent.parent.name + ":" + keyname
                d[keyname] = child.text
            else:
                get_raw_data(child, data)
    if d:
        data.append(d)

def convert_xml_to_csv(tag):
    data = []
    get_raw_data(tag, data)
    file = open("result.csv", "a")
    cw = csv.writer(file, delimiter="\t")
    for row in data:
        cw.writerows(row.viewitems())
    file.write("\n\n")
    file.close()

for element in all_td:
    if "13F" in element.text:
        list_of_all_13f_links.append(element.next_sibling.next_sibling.a.get("href"))

for link in list_of_all_13f_links:
    get_details(link)

for url in list_of_txt_urls_to_parse:
    txt = urllib2.urlopen(url)
    xml = BeautifulSoup(txt, "xml").XML
    if xml:
        for tag in xml.find_all(True, recursive=False):
            convert_xml_to_csv(xml)


# this is test data that can be removed
# url = "https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt"
# txt = urllib2.urlopen(url)
# xml = BeautifulSoup(txt, "xml").XML
# for tag in xml.find_all(True, recursive=False):
#     convert_xml_to_csv(tag, 3)
# end test data

# edgarSubmission: get rid of this as parent
# get other XML too!
# create an input feature
