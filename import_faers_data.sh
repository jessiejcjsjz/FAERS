#!/bin/bash

# Unzip and import data into sqlite database.
for filename in data/*.zip; do
  unzip -o $filename -d data/
  echo "`date`: begninning import for $filename"
  echo "Importing DRUG table..."
  find data/ -iname DRUG*txt | xargs -I % python import_data.py %
  echo "Importing DEMO table..."
  find data/ -iname DEMO*txt | xargs -I % python import_data.py %
  echo "Importing INDI table..."
  find data/ -iname INDI*txt | xargs -I % python import_data.py %
  echo "Importing OUTC table..."
  find data/ -iname OUTC*txt | xargs -I % python import_data.py %
  echo "Importing REAC table..."
  find data/ -iname REAC*txt | xargs -I % python import_data.py %
  echo "Importing RPSR table..."
  find data/ -iname RPSR*txt | xargs -I % python import_data.py %
  echo "Importing THER table..."
  find data/ -iname THER*txt | xargs -I % python import_data.py %

  # Clean up files.
  find data/ -name '*txt' -exec rm {} \;
  find data/ -name '*pdf' -exec rm {} \;
  find data/ -name '*doc' -exec rm {} \;
  rm -rf ./data/sgml
  rm -rf ./data/sqml
  rm -rf ./data/as*
  rm -rf ./data/ASCII
done;

## Create indisces on DRUG and REAC to speed up merging.
sqlite3 faers.db "CREATE INDEX drugs_idx ON drug (primaryid, drugname)"
sqlite3 faers.db "CREATE INDEX reacs_idx ON reac (primaryid, pt)"
sqlite3 faers.db "CREATE INDEX demos_idx ON demo (reporter_country, event_dt)"
