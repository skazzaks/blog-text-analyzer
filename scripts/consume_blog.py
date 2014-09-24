#!/usr/bin/python

# Author: Devon Fritz
# This script takes a file of RSS feed URLs and pulls down all of the posts from them
import sys
import feed_helpers
import shlex

if len(sys.argv) != 4:
    sys.exit("""Incorrect Parameters! Exiting
                Usage:  consume_blog <input file> <output dir> <language>""")
    
inputfile = sys.argv[1]
outputdir = sys.argv[2]
language = sys.argv[3]
results = []
with open(inputfile) as f:
    lines = f.readlines()
    # Skip comment lines
    # Read in all others with the values:
    # URL  SITE SEX LANGUAGE
    for l in lines:
        if l[0] != "#":
            result = shlex.split(l)
            results.append(result)

# Now that we read in the results, let's pull down the files for each entry
# using the helper class
for r in results:
    feed_helpers.downloadFeedEntries(r[0], outputdir, "#" + r[0] + " " + r[1] +  " " + r[2] + " " + language + "\n")
