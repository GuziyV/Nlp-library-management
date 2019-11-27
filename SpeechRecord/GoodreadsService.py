import os
import requests
import xml.etree.ElementTree as ET
from xml.etree import ElementTree

import xmltodict

base = "https://www.goodreads.com"
searchEndp = "/search/index.xml"
key = "HWhaO97bSHYSNloJ67lig"
separator = " | "


def etree_to_dict(t):
    d = {t.tag: map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d

class GoodreadsService:


    def SearchByKeywords( self, args ):
        argsParam = separator.join(args)
        payload = { 'key': key, 'q':argsParam }
        url = base + searchEndp

        response = requests.get(url,params=payload)
        return  response

    def addBook(self, args):
        bookResponse = self.SearchByKeywords(args)
        xmlRoot =  ElementTree.ElementTree(ET.fromstring(bookResponse.text.encode('utf-8')))


        booksArray = []

        for x in xmlRoot.getroot()[1][6]:# feel free to provide easier way to get complex objects
            yolo = dict()
            for what in x._children:
                yolo[what.tag] = what.text
            book = dict()
            for oops in x._children[8]:
                book[oops.tag] = oops.text
            yolo['best_book'] = book;
            booksArray.append(yolo)
        dafq = '2'
