#!/bin/bash
  
echo "Searching for new files..."

if [ ! -d "data/" ]; then
  mkdir "data/"
fi

python get_raw_data_links.py > tmp.txt

if [ "$(ls data/)" ]; then
  echo "Directory is not empty"
  CURRENT_FILES=$(ls data/)
  NEW_FILES=$(grep -v -F "${CURRENT_FILES}" tmp.txt)
else
  echo "Directory is empty; using tmp.txt"
  NEW_FILES=$(cat tmp.txt)  
fi

echo "${NEW_FILES}" | xargs -I % wget -P data/ %
rm tmp.txt
