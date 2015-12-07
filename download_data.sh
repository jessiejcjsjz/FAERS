#!/bin/bash
# Check if data directory exists, create if not.
if [ ! -d "data/" ]; then
  mkdir "data/"
fi

# Fetch links to data.
python get_data_links.py > tmp.txt

# Only download files that are not in data/
if [ "$(ls data/)" ]; then
  echo "Directory is not empty"
  CURRENT_FILES=$(ls data/)
  NEW_FILES=$(grep -v -F "${CURRENT_FILES}" tmp.txt)
else
  echo "Directory is empty; using tmp.txt"
  NEW_FILES=$(cat tmp.txt)  
fi

# wget the new files
echo "${NEW_FILES}" | xargs -I % wget -P data/ %
rm tmp.txt
