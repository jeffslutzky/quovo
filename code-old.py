from lxml import html, etree
import requests
import pdb

cik = "0001166559"

url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK={}&owner=exclude&action=getcompany&Find=Search".format(cik)

page = requests.get(url)
tree = html.fromstring(page.content)

# print page.content

list_to_parse = tree.xpath('//td')
list_of_all_13f = []

for element in list_to_parse:
    if element.text and "13F" in element.text:
        list_of_all_13f.append(element)

for element in list_of_all_13f:
    pdb.set_trace()


# <tr>
# <td nowrap="nowrap">13F-HR</td>

# <td nowrap="nowrap"><a href="/Archives/edgar/data/1166559/000104746911000932/0001047469-11-000932-index.htm" id="documentsbutton">&nbsp;Documents</a></td>

# <td class="small" >Quarterly report filed by institutional managers, Holdings<br />Acc-no: 0001047469-11-000932&nbsp;(34 Act)&nbsp; Size: 8 KB            </td>
#             <td>2011-02-14</td>
#             <td nowrap="nowrap"><a href="/cgi-bin/browse-edgar?action=getcompany&amp;filenum=028-10098&amp;owner=exclude&amp;count=40">028-10098</a><br>11610035         </td>
#  </tr>
