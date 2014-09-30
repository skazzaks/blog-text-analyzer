#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Devon Fritz
# Date: 24.9.14
# Analyzes the diabetes data in a variety of ways

import sys
import os
import nltk
from os import path
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.collocations import *
import codecs
import string
import re
import shlex

# Methods
def generateWordCloud(text, stop):
    d = path.dirname(outputdir)

    for w in stop:
        STOPWORDS.add(w)

    # Generate the wordcloud without the stop words    
    wordcloud = WordCloud(stopwords=STOPWORDS).generate(text)

    # Draw the positioned words to a PNG file.
    wordcloud.to_file(path.join(d, 'diabetes-wordcloud.png'))
    

def doc_features(word_features, datafolder, doc):
    with codecs.open(datafolder + "/" + thefile) as f:
        doc_words = set(doc)
        features ={}
        for w in word_features:
            features['contains(%s)' % w] = (w in doc_words)
    return features



if len(sys.argv) != 3:
    sys.exit("""Incorrect Parameters! Exiting
                Usage:  analyze_data <data folder> <output dir>""")

datafolder = sys.argv[1]
outputdir = sys.argv[2]

# Load in the text
print 'Reading in all files'
text = ""

for root, dirs, files in os.walk(datafolder, topdown=True):
    for thefile in files:
        with codecs.open(datafolder + "/" + thefile) as f:
            # Skip the header
            f.readline()
            thisfile = f.read()
            text += thisfile

# Post process some problems we had


text = text.lower()
# Compile and remove stop words
print 'Compiling and removing stop words'
stop = stopwords.words('english')
stop = stop + stopwords.words('german')
stop += ['nbsp', 'm', 'thing', 'multiple', 'ber', 'f', 'mal', 'font family', 'k', 'l']
stop += ['h', 'l', 'u', 'one', 'us', 'new', 'mso', 'schon', 'ja', 'two', 'mehr', 'dass', 'n\'t', 'like']
stop += ['people', 'get', 'would']
stop += ['ganz', 'andreas', 'gibt', 'neue', 'beim', 'gut', 'tag', 'viele', 'einfach', 'mal']
stop += ['uhr', 'ab', 'ger', 'immer', 'heute', 'eigentlich', 'w', 'zeit', 'e', 'n', 'wirklich', 'neuen', 'geht', 'wurde', 'nnen', 'zwei', 'abbott', 'erst', 'blog', 'hallo', 'seit', 'letzten', 'sei', 'en', 'leider']
stop += ['chris', 'miss', 'questions', 'joe', 'center', '2014', '2013', '8220', '8221']
stop += ['iam_spartacus', '8217', 'll', 'please', 'contact', 'a.m.', 'sixuntilme.com']
stop += ['2010', '2011', '2012']
stop += ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
stop += ['site', 'navigate', 'web', 'internet', 'reader', 'article', 'feed', 'articles', 'kerri', 'reader']
stop += ['§', '1', 'abs', 'ag', 'r', 'nr', '69', 'g4', 'sb', '15', '50', '9', 'www.diabetes-blog.at']
stop += ['xi', 'b', '15.1', 'rss', 'eintrag', '43250', 'www.diabetes-blog.at', 'leben', '1.0', '2.0']
stop += ['r', 'b', 'sgb', '3', 'abs.', 'ix', '16', 'v', 'tuut', '2', '18', '14']
stop += ['januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'dezember']
stop += ['g', '8', '5', '6', '7', '4', 'p', 'd']
stop += list(string.punctuation)

stop_tokens = []
for w in stop:
    stop_tokens += nltk.word_tokenize(w)


# Generate a word cloud
print 'Generating Word Cloud'
generateWordCloud(text, stop)


# Find collocations - window 5
tokens = nltk.word_tokenize(text)
tokens = [t for t in tokens if t not in stop_tokens]
#print tokens[:100]
#fdist1 = nltk.FreqDist(tokens)
#print fdist1.freq('table.msonormaltable')

print 'Generating Collocations with Window Size 5'
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens, window_size = 5)
a= finder.nbest(bigram_measures.likelihood_ratio, 200)
doc = ""

f = open(outputdir + "/collocations-window5", "w")
for pair in a:
    f.write(pair[0] + ": "+ pair[1] + "\n")
f.close()

# Find collocations - window 2
print 'Generating Collocations with Window Size 2'
finder = BigramCollocationFinder.from_words(tokens, window_size = 2)
a= finder.nbest(bigram_measures.likelihood_ratio, 200)

f = open(outputdir + "/collocations-window2", "w")
for pair in a:
    f.write(pair[0] + " " + pair[1] + "\n")
f.close()

# Take the top non stop words in the document and classify to see
# if there are differences between what people write about

print 'Classifying articles based on sex'
# Grab the top 2000 occurring words
freqWords = nltk.FreqDist(tokens)
feat = [f for f in freqWords.keys()[:2000] if len(f) > 3]
features = {}
docs =  []
for root, dirs, files in os.walk(datafolder, topdown=True):
    for thefile in files:
        with codecs.open(datafolder + "/" + thefile) as f:
            header = f.readline()
            h = shlex.split(header[1:])
            sex = h[2]
            docs.append([thefile, sex])
#print docs

featuresets = [(doc_features(feat, datafolder, d), c) for (d, c) in docs]
#print featuresets
classifier = nltk.NaiveBayesClassifier.train(featuresets)

classifier.show_most_informative_features(10)

     
    


