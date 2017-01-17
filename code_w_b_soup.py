from bs4 import BeautifulSoup, NavigableString
import urllib2
import pdb
import csv
import sys

cik = "0001166559"

url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&Find=Search".format(cik)

page = urllib2.urlopen(url)
html = BeautifulSoup(page, "lxml")

list_of_all_13f_links = []

all_td = html.find_all("td")

# don't delete this!
#
# def get_details(link):
#     detail_url = "https://www.sec.gov{}".format(link)
#     detail_page = urllib2.urlopen(detail_url)
#     detail_html = BeautifulSoup(detail_page, "lxml")
#     for anchor in detail_html.find_all("a"):
#         url = "https://www.sec.gov{}".format(anchor.get("href"))
#         if ".txt" in url:
#             txt = urllib2.urlopen(url)
#             xml = BeautifulSoup(txt, "xml").xml
#             # print xml
#
#
# for element in all_td:
#     if "13F" in element.text:
#         list_of_all_13f_links.append(element.next_sibling.next_sibling.a.get("href"))
#
# for link in list_of_all_13f_links:
#     get_details(link)

test_txt_url = "https://www.sec.gov/Archives/edgar/data/1166559/000110465916156931/0001104659-16-156931.txt"

txt = urllib2.urlopen(test_txt_url)
xml = BeautifulSoup(txt, "xml").XML


def convert_to_csv(xml):
    data = []
    cols = []
    for tag in xml.find_all(True, recursive=False):
        # print tag.name
        d = {}
        for child in tag:
            if hasattr(child, "name") and not isinstance(child, NavigableString):
                d[child.name] = child.text
                # print "{} = {}".format(d[child.name], child.text)
        data.append(d)
        cols = d.keys()
        cw = csv.writer(open("result.csv",'w'))
        # cw.writerow(data)
        for row in data:
            cw.writerow([row.get(k, 'N/A') for k in cols])

convert_to_csv(xml)



# print xml
