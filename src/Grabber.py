import requests
from requests_html import HTMLSession
import sys
import re

from src import Utils

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

url = "http://www.dgsi.pt"
mainPagePath = "/jstj.nsf?OpenDatabase"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}


def getDataFromLink(link):
    session = HTMLSession()
    response = session.get(link, headers=headers)
    response.html.encoding = 'ISO-8859-1'
    table = response.html.find('table')[0]

    tabledata = [[c.text for c in row.find('td')] for row in table.find('tr')][0:]
    court = tabledata[0][1]
    tabledata = tabledata[1:]
    tableheader = ['Link','Tribunal']
    tablefields = [[link],[court]]
    for col in tabledata:
        header = col[0].replace(":", "")
        fields = []
        if header == "Descritores":  # Porque aparecem separados por \n
            for row in col[1:]:
                temp = row.split("\n")
                for item in temp:
                    if item != "":
                        fields.append(item)
        else:
            for row in col[1:]:
                if row != "":
                    fields.append(row)
        if header == "Decisão Texto Integral":
            fields[0] = Utils.clearEnters(fields[0])
            fields[0] = re.sub(' +', ' ', fields[0])
        if header != "" and fields != []:
            tableheader.append(header)
            fields = [*set(fields)]
            tablefields.append(fields)

    res = dict(zip(tableheader, tablefields))
    return res


def getMultipleFromMainPage():
    request = requests.get(url + mainPagePath, headers=headers)

    print("Status code: " + str(request.status_code))
    if request.status_code != 200:
        print('Error on connection to webpage', file=sys.stderr)
        exit()

    htmlSplitted = request.text.replace("<", " ") \
        .replace(">", " ") \
        .split(" ")
    links = []

    for string in htmlSplitted:
        if "href=\"" in string and "jstj.nsf/" in string:
            string = string.split("\"")[1]
            links.append(string)

    links.pop(0)
    print("Found " + str(len(links)) + " links")

    i = 0
    for link in links:
        print("Working on: " + url + link)
        Utils.saveData("jsons", Utils.createJsonSchemaFromRawSchema(getDataFromLink(url + link)))
        i += 1


def getFromList(list):
    print(list)
    for link in list:
        Utils.saveData("doc_json", Utils.createJsonSchemaFromRawSchema(getDataFromLink(link)))
