#!/bin/bash

python -c "import BeautifulSoup"
if [ $? -ne 0 ]; then
  echo "Please install the BeautifulSoup Python module..."
  exit
fi

python -c "import urllib2"
if [ $? -ne 0 ]; then
  echo "Please install the urllib2 Python module..."
  exit
fi
  
echo "Searching for new files..."

if [ ! -e "get_links.py" ]; then
  echo "The file get_links.py does not exist! Exiting..."
  exit
fi

if [ ! -d "zip/" ]; then
  mkdir "zip/"
fi

python get_links.py > tmp.txt

if [ "$(ls zip/)" ]; then
  echo "Directory is not empty"
  CURRENT_FILES=$(ls zip/)
  NEW_FILES=$(grep -v -F "${CURRENT_FILES}" tmp.txt)
else
  echo "Directory is empty; using tmp.txt"
  NEW_FILES=$(cat tmp.txt)  
fi

echo "${NEW_FILES}" | xargs -I % wget -P zip/ %
rm tmp.txt
