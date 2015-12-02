# FDA Adverse Event Reporting System

This repo provides scripts to download, process, and analyze adverse event data from the [FDA Adverse Event Reporting System](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/). The data is stored in a [SQLite](https://www.sqlite.org/) database.

## Instructions

#### 1. Install [SQLite](https://www.sqlite.org/)
`sudo apt-get install sqlite`

#### 2. Install [BeautifulSoup](https://pypi.python.org/pypi/BeautifulSoup/3.0.5)
`sudo pip install BeautifulSoup` or `sudo apt-get install python-beautifulsoup`

#### 3. Install [urllib2](https://docs.python.org/2/library/urllib2.html)
`sudo pip install urllib3`or `sudo apt-get install python-urllib3`

#### 4. Download and import FDA data from [FDA AERS](http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/AdverseDrugEffects/)
`./download.sh`
`./import_faers_data.sh`

## Questions/issies/contact
mlbernauer@gmail.com
