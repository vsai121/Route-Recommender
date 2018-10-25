import pandas as pd
import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs
import http.cookiejar

from time import sleep
from time import time
from random import randint



start_time = time()
requests = 0
mainUrl = "https://www.google.co.in/search?q="


def getFlightUrl(mainUrl , place1 , place2):
    return mainUrl + place1 + "+" + place2 + "+" + "flights"


def getTrainUrl(mainUrl , place1 , place2):
    return mainUrl + place1 + "+" + place2 + "+" + "trains"

def getPage(url):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    cookie = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)

    try:
        request = urllib.request.Request(url = url , headers=headers)
        page = opener.open(request)

    except HTTPError as e:
        return None

    return page


def extractFlightData(bsObj):

    result = bsObj.select(".ADuBqd")

    if(result == []):
        result = bsObj.select(".Crs1tb")

        if result == []:
            result = bsObj.select(".di3YZe")



def extractTrainData(bsObj):

    result = bsObj.select(".ccBEnf")

    return result

def checkFlights(place1 , place2):

    global requests

    url = getFlightUrl(mainUrl , place1 , place2)
    print(url)
    page = getPage(url)

    sleep(randint(1,5))
    requests += 1

    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

    if page.status != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    if requests > 100:
        warn('Number of requests was greater than expected.')

    if page==None:
        print("Error reading page")


    html = page.read()
    bsObj = bs(html , "lxml")

    result = extractFlightData(bsObj)

    if result == []:
        print("No flights available between " + place1 + " and  " + place2)

    else:

        print("Flights available between " + place1 + " and  " + place2)



def checkTrains(place1 , place2):

    global requests

    url = getTrainUrl(mainUrl , place1 , place2)
    print(url)
    page = getPage(url)

    sleep(randint(1,5))
    requests += 1

    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

    if page.status != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    if requests > 100:
        warn('Number of requests was greater than expected.')

    if page==None:
        print("Error reading page")


    html = page.read()
    bsObj = bs(html , "lxml")

    result = extractTrainData(bsObj)

    if result == []:
        print("No trains available between " + place1 + " and  " + place2)

    else:

        print("Trains available between " + place1 + " and  " + place2)


def getInput(places):

    n = int(input('Enter number of places:'))
    for i in range(0, n):
        x = input('Enter the place: ')
        places.append(x)


if __name__ == "__main__":

        places = []

        getInput(places)

        for i in range(len(places) - 1):

            checkFlights(places[i] , places[i+1])
            checkTrains(places[i] , places[i+1])
