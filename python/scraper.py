import bs4
import requests
from urllib.request import urlopen
import json
import datetime
import time
import csv

#pgeocode is python lib for zip code mapping things...check it out
# get urls of "more concerts" pages if there are more than 10 concerts on that given day
def getLinks(metroURL):
    try:
        page = urlopen(metroURL)
    except:
        print("Error opening the URL")
        pass
    else:
        soup = bs4.BeautifulSoup(page, "html.parser")
        # go to the more concerts page (if there are more than 10 on that day)
        more = []
        for dates in soup.find_all(class_="more-concerts-element"):
            string = 'https://www.songkick.com' + dates.a.get('href')
            more.append(string)
        return more

def getShows(URL):
    try:
        page = urlopen(URL)
    except:
        print("Error opening the URL")
        pass
    else:
        soup = bs4.BeautifulSoup(page, "html.parser")
        showList = []
        for venues in soup.find_all(type="application/ld+json"):
            str = venues.string
            str = str[1:-1]
            data = json.loads(str)
            if data.__contains__("startDate") & data.__contains__("location") & data.__contains__("performer"):
                show = {}
                show['Date'] = data["startDate"][0:10]
                show['Year'] = data["startDate"][0:4]
                show['Month'] = data["startDate"][5:7]
                show['Day'] = data["startDate"][8:10]
                show['Venue'] = data["location"]["name"]
                artists = []
                for i in data["performer"]:
                    artists.append(i["name"])
                show['Artists'] = artists
                showList.append(show)
        return showList

# old
# performers = []
# for i in jsn['performer']:
#     performers.append(i['name'])
# show['performers'] = performers
# date = jsn['startDate'].split('-')
# show['year'] = date[0]
# show['month'] = date[1]
# show['day'] = date[2][0:2]
#
# show['venue'] = jsn['location']['name']
# shows.append(show)

def getMetro(metro):
    base = 'https://www.songkick.com/metro-areas/' + str(metro)
    showList = []
    for idx in range(1, 100, 1):
        url = base + '?page=' + str(idx) + '#metro-area-calendar'
        shows = getShows(url)
        if len(shows) == 0:
            break
        for i in shows:
            showList.append(i)
        links = getLinks(url)
        for i in links:
           for j in getShows(i):
                showList.append(j)

    return showList

def artistList(shows):
    artists = []
    for i in shows:
        for j in i["Artists"]:
            artists.append(j)
    uniq = []
    [uniq.append(x) for x in artists if x not in uniq]
    return uniq

def venueList(shows):
    venues = []
    for i in shows:
        venues.append(i["Venue"])
    uniq = []
    [uniq.append(x) for x in venues if x not in uniq]

    indexed = []
    for i in uniq:
        indexed.append([i, venues.count(i)])

    indexed.sort(key=lambda row: row[1], reverse=True)
    return indexed

if __name__ == '__main__':
    showList = getMetro(9480)
    print(len(showList), " upcoming shows")
    for i in showList:
        if int(i["Month"]) == 1:
             [print("Artist:", i["Artists"][0], "\tDate:", i["Date"], "\tVenue:", i["Venue"]) for i in showList if int(i["Month"]) == 1]