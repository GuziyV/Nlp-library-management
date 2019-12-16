import os
import requests
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import  urllib.parse as  urllib
import OAuthService
import xml.dom.minidom


base = "https://www.goodreads.com"

searchEndp = "/search/index.xml"
listShelfEndp = "/shelf/list.xml"
addShelfEndp =  "/user_shelves.xml"
addBookToShelfEndp = "/shelf/add_to_shelf.xml"
getShelfBooksEndp = "/review/list.xml?v=2"
getBookByIdEndp = '/book/show.xml'
reviewEndp = '/review.xml'

key = "IC5itDAhtayZ9ZIRc77qrQ"
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
        print('Searching for ' + ' '.join(args))
        argsParam = separator.join(args)
        payload = { 'key': key, 'q':argsParam }
        url = base + searchEndp

        response = requests.get(url,params=payload)
        parsedResp = self.parseXmlBooksRespone(response.text)
        return  parsedResp

    def getBookId(self, keywords):
        books = self.SearchByKeywords(keywords);
        print("Getting id for a book: " + books[0]['best_book']['title']);
        bookId = books[0]['best_book']['id']
        return  bookId;

    def addBook(self, args):
        booksArray = self.SearchByKeywords(args)

        print("Adding book to a shelf: " + booksArray[0]['best_book']['title']);

        body = urllib.urlencode({'name': shelfName, 'book_id': booksArray[0]['best_book']['id']})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + addBookToShelfEndp
        response, content = self.clientOauth.request(url,
                                           'POST', body, headers)
        print(response)

    def getBookById(self,id):
        url = base + getBookByIdEndp;
        payload = {'key': key, 'format': 'xml', 'id': id}
        response = requests.get(url, params=payload)
        parsedResp = self.parseXmlBookRespone(response)
        dfq = 2
        return parsedResp

    def removeBook(self, id):
        body = urllib.urlencode({'name': shelfName, 'book_id': id, 'a' : 'remove'})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + addBookToShelfEndp
        book = self.getBookById(id);
        print("Removing book from shelf: " + book['title']);
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
        return self.clientOauth.request(url,'POST', body, headers)


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
        xmlRoot = ElementTree.ElementTree(ET.fromstring(response))

        booksArray = []

        for x in xmlRoot.getroot()[1][6]:  # feel free to provide easier way to get complex objects
            yolo = dict()
            for what in x:
                yolo[what.tag] = what.text
            book = dict()
            for oops in x[8]:
                book[oops.tag] = oops.text
            yolo['best_book'] = book;
            booksArray.append(yolo)
        return booksArray;

    def addReview(self, text, id):
        book = self.getBookById(id)
        print('Adding review for ' + book['title'] )
        body = urllib.urlencode({'review[review]': text, 'book_id': id})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = base + reviewEndp
        return self.clientOauth.request(url, 'POST', body, headers)

    def parseXmlBookRespone(self, response):
        xmlRoot = ElementTree.ElementTree(ET.fromstring(response.encode('utf-8')))

        book =  xmlRoot.getroot()[1] # feel free to provide easier way to get complex objects
        yolo = dict()
        for what in book:
            yolo[what.tag] = what.text
        return yolo;

