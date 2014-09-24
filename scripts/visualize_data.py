#!/usr/bin/python

import sys
import feed_helpers
import shlex
import nltk
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

if len(sys.argv) != 3:
    sys.exit("""Incorrect Parameters! Exiting
                Usage:  visualize_data <data folder> <output dir>""")
    
datafolder = sys.argv[1]
outputdir = sys.argv[2]

url_map = {}
sex_map = {}
orgtype_map = {}
lang_map = {}

# Go through each file in the specified folder and read the files in
for root, dirs, files in os.walk(datafolder, topdown=True):
    for thefile in files:
        with open(datafolder + "/" + thefile) as f:
            
            # Read in header
            header = f.readline()
            h = shlex.split(header[1:])
            url = feed_helpers.getDomainOfUrl(h[0])
            orgtype = h[1]
            sex = h[2]
            lang = h[3]
            
            # Read the rest of the file and tokenize
            wordcount = len(nltk.word_tokenize(f.read()))

            # update maps with the new values
            if(url not in url_map):
                url_map[url] = 0
            url_map[url] += wordcount

            if(orgtype not in orgtype_map):
                orgtype_map[orgtype] = 0
            orgtype_map[orgtype] += wordcount

            if(sex not in sex_map):
                sex_map[sex] = 0
            sex_map[sex] += wordcount

            if(lang not in lang_map):
                lang_map[lang] = 0
            lang_map[lang] += wordcount

# Final maps of the data               
print lang_map
print sex_map
print orgtype_map
print url_map

a = []
b = []
for k,v in lang_map.items():
    a.append(k)
    b.append(int(v))

print a
print b
size = len(a)
pos = arange(size) + .5
rects1 = bar(pos, b, align = 'center', color = '#a1f1d1')
xticks(pos, a)
xlabel('Language')
ylabel('Word Count')
title('Word Counts by language')
savefig('foo.png') 
show()



    



