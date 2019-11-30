import os
import requests
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import urllib
import OAuthService
import xml.dom.minidom

import xmltodict

base = "https://www.goodreads.com"

searchEndp = "/search/index.xml"
listShelfEndp = "/shelf/list.xml"
addShelfEndp =  "/user_shelves.xml"
addBookToShelfEndp = "/shelf/add_to_shelf.xml"
getShelfBooksEndp = "/review/list.xml?v=2 "

key = "HWhaO97bSHYSNloJ67lig"
shelfName = 'mybooks'

separator = " | "


def etree_to_dict(t):
    d = {t.tag: map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d

class GoodreadsService:
    clientOauth = {}

    def __init__(self):
        serv = OAuthService.OAuthService()
        self.clientOauth  = serv.getClient();

    def SearchByKeywords( self, args ):
        argsParam = separator.join(args)
        payload = { 'key': key, 'q':argsParam }
        url = base + searchEndp

        response = requests.get(url,params=payload)
        return  response

    def addBook(self, args):
        bookResponse = self.SearchByKeywords(args)
        booksArray = self.parseXmlBooksRespone(bookResponse);

        print("Adding book to a shelf: " + booksArray[0]['best_book']['title']);

        body = urllib.urlencode({'name': shelfName, 'book_id': booksArray[0]['best_book']['id']})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + addBookToShelfEndp
        response, content = self.clientOauth.request(url,
                                           'POST', body, headers)
        print(response)


    def removeBook(self, id):
        body = urllib.urlencode({'name': shelfName, 'book_id': id, 'a' : 'remove'})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + addBookToShelfEndp
        response, content = self.clientOauth.request(url,
                                           'POST', body, headers)
        print(response)

    def getUserId(self):
        url = base + '/api/auth_user'
        response, content = self.clientOauth.request(url, 'GET')

        userxml = xml.dom.minidom.parseString(content)
        user_id = userxml.getElementsByTagName('user')[0].attributes['id'].value
        return str(user_id)

    def createShelf(self):
        body = urllib.urlencode({'user_shelf[name]': shelfName})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + addShelfEndp
        self.clientOauth.request(url,'POST', body, headers)


    def listShelfs(self):
        url = base + '/shelf/list.xml'
        id = self.getUserId()
        payload = {'key': key, 'user_id': id}
        response = requests.get(url, params=payload)
        print(response.text)

    def getShelfBooks(self):
        id = self.getUserId()

        payload = {'key': key, 'user_id': id, 'shelf':shelfName}
        body = urllib.urlencode(payload)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + getShelfBooksEndp
        response, content = self.clientOauth.request(url,'GET', body,headers)
        print(response['status'])
        print(content)

    def parseXmlBooksRespone(self, response):
        xmlRoot = ElementTree.ElementTree(ET.fromstring(response.text.encode('utf-8')))

        booksArray = []

        for x in xmlRoot.getroot()[1][6]:  # feel free to provide easier way to get complex objects
            yolo = dict()
            for what in x._children:
                yolo[what.tag] = what.text
            book = dict()
            for oops in x._children[8]:
                book[oops.tag] = oops.text
            yolo['best_book'] = book;
            booksArray.append(yolo)
        return booksArray;

