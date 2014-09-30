import numpy as np
import matplotlib.pyplot as plt
from pylab import *

# Author: Devon Fritz
# Date: 2014.16.9
# Common code for outputting nice graphs

def makeBarGraph(mapbar, ishbar, graphxlabel, graphylabel, graphtitle, outputdir, outputfilename):
    mapbarnames = []
    mapbarvalues = []
    
    for k,v in mapbar.items():
        mapbarnames.append(k)
        mapbarvalues.append(int(v))
        
    size = len(mapbarnames)
    pos = arange(size) + .5
    figure(num=None, figsize=(6, 4.5), dpi=80, facecolor='w', edgecolor='k')

    clf()
    if(ishbar):
        rects1 = barh(pos, mapbarvalues, align = 'center', color = '#a1f1d1')
    else:
        rects1 = bar(pos, mapbarvalues, align = 'center', color = '#a1f1d1')

    xticks(pos, mapbarnames)
    xlabel(graphxlabel)
    ylabel(graphylabel)
    title(graphtitle)
    savefig(outputdir + outputfilename)
