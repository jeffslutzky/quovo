from bs4 import BeautifulSoup, NavigableString
import urllib2
import csv
import sys

cik = raw_input("Enter a ticker or symbol: ")

url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&Find=Search".format(cik)

list_of_13f_links = []
list_of_txt_urls_to_parse = []

def check_url(url):
    page = urllib2.urlopen(url)
    if "No matching Ticker Symbol." in page.read():
        print "No matching ticker symbol."
        sys.exit()
    else:
        get_data(url)

def get_data(url):
    print "Working..."

    page = urllib2.urlopen(url)

    html = BeautifulSoup(page, "lxml")
    all_td = html.find_all("td")

    for element in all_td:
        if "13F" in element.text:
            list_of_13f_links.append(element.next_sibling.next_sibling.a.get("href"))

    if not list_of_13f_links:
        print "No 13F reports found."
        sys.exit()

    for link in list_of_13f_links:
        get_txt_urls(link)

    for url in list_of_txt_urls_to_parse:
        txt = urllib2.urlopen(url)
        xml = BeautifulSoup(txt, "xml").edgarSubmission
        if xml:
            for tag in xml.find_all(True, recursive=False):
                convert_xml_to_csv(xml)

    print "Done! Results are at result.csv in this directory."

def get_txt_urls(link):
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
                keyname = child.name
                child_text = child.text
                while child.parent.name != "edgarSubmission":
                    keyname = child.parent.name + ":" + keyname
                    child = child.parent
                d[keyname] = child_text
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


check_url(url)
