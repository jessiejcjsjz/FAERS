#!/usr/bin/python
#########################################################
# Michael Bernauer
# 2014/12/22
# Run this script to retrieve data from the FDA
# FAERS website. This will download all into a folder
# called "faers_data" located in the current directory.
#
# Running the script: ./faers_data_retriever.py
#
#########################################################


from BeautifulSoup import *
import urllib2

BASE_URL="http://www.fda.gov"
PARENT_PAGE="http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/ucm083765.htm"

def get_data_links(page):
    """ This function will scan the parent page for links to FDA AERS
        data an print the found links. These links can be saved to 
        a text file and used to download the data.
    """
    data_links = set()
    try:
        c = urllib2.urlopen(page)    
    except:
        pass
    soup = BeautifulSoup(c.read())
    links = soup('a')
    for link in links:
        d = dict(link.attrs)
        if 'href' in d and ".zip" == d['href'][-4:]:
            data_links.add("%s%s" % (BASE_URL, d['href']))
    for i in data_links: print i

get_data_links(PARENT_PAGE)
