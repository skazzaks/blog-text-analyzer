#!/usr/bin/python

# 29.8.14 Devon Fritz
# Helper functions for getting feeds

import sys
import feedparser
import re
import datetime
import requests
from lxml.html import clean
from readability.readability import Document

# Downloads all of the posts from the given url feed into the
# specified output directory
def downloadFeedEntries(rootFeedURL, outputDir, headerLine):
    f = feedparser.parse(rootFeedURL)
    # Pull down and store the content of each feed
    i = 0
    for e in f.entries:
        # Test for content attribute
        # If present, use it
        if 'content' in e:
            text = e.content[0].value
        # If not, pull the content from the link
        else:
            text = Document(requests.get(e.link).content).summary()
            text = clean.clean_html(text)
    
        newfile = open(outputDir + "%s%s" % (getDomainOfUrl(rootFeedURL), str(i)), "w")
        text = scrubText(text).encode("utf-8")
        newfile.write(headerLine)
        newfile.write(text)
        newfile.close()
        i = i + 1

def getDomainOfUrl(url):
    r = re.compile('.*//(.+?)/.*')
    return r.match(url).group(1)
    
def scrubText(text):
    return removeExtraSpaces(removeHtmlTags(text))

def removeHtmlTags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def removeExtraSpaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)
