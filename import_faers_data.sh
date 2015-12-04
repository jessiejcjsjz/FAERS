#!/bin/bash
DRUG="CREATE TABLE DRUG (ISR INT,DRUG_SEQ INT,ROLE_CODE TEXT,DRUGNAME TEXT,VAL_VBM INT,ROUTE TEXT,DOSE_VBM TEXT,DECHAL TEXT,RECHAL TEXT,LOT_NUM CHAR,EXPT_DT INT,NDA_NUM TEXT);" DEMO="CREATE TABLE DEMO (ISR INT,CASE_NUM INT,IF_CODE TEXT,FOIL_SEQ TEXT,IMAGE TEXT,EVENT_DT INT,MFR_DT INT,FDA_DT INT,REPT_CODE TEXT,MFR_NUM TEXT,MFR_SNDR TEXT,AGE REAL,AGE_CODE TEXT,GNDR_CODE TEXT,E_SUB TEXT,WT REAL,WT_CODE TEXT,REPT_DT INT,OCCP_CODE TEXT,DEATH_DT INT,TO_MFR TEXT,ONFID TEXT,REPORTER_COUNTRY TEXT);"
INDI="CREATE TABLE INDI (ISR INT,DRUG_SEQ INT,INDI_PT TEXT);"
OUTC="CREATE TABLE OUTC (ISR INT,OUT_CODE TEXT);"
REAC="CREATE TABLE REAC (ISR INT,PT TEXT);"
RPSR="CREATE TABLE RPSR (ISR INT,RPSR_CODE TEXT);"
THER="CREATE TABLE THER (ISR INT,DRUG_SEQ INT,START_DT INT,END_DT INT,DUR INT,DUR_CODE TEXT);"

if [ -e "faers.db" ]; then
  rm faers.db
fi

sqlite3 faers.db "${DRUG}"
sqlite3 faers.db "${DEMO}"
sqlite3 faers.db "${INDI}"
sqlite3 faers.db "${OUTC}"
sqlite3 faers.db "${REAC}"
sqlite3 faers.db "${RPSR}"
sqlite3 faers.db "${THER}"

chmod +w faers.db

# Unzip and import data into sqlite database.
for filename in data/*.zip; do
  echo "`date`: beginning load for $filename"
  unzip -o $filename -d data/  
  find -name DRUG*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' DRUG"
  find -name DEMO*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' DEMO"
  find -name INDI*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' INDI"
  find -name OUTC*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' OUTC"
  find -name REAC*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' REAC"
  find -name RPSR*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' RPSR"
  find -name THER*TXT | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' THER"
  rm -rf ./data/ascii
done;

# Delete header rows.
sqlite3 faers.db "DELETE FROM DRUG WHERE ISR = 'ISR'"
sqlite3 faers.db "DELETE FROM DEMO WHERE ISR = 'ISR'"
sqlite3 faers.db "DELETE FROM INDI WHERE ISR = 'ISR'"
sqlite3 faers.db "DELETE FROM OUTC WHERE ISR = 'ISR'"
sqlite3 faers.db "DELETE FROM REAC WHERE ISR = 'ISR'"
sqlite3 faers.db "DELETE FROM RPSR WHERE ISR = 'ISR'"
sqlite3 faers.db "DELETE FROM THER WHERE ISR = 'ISR'"

# Create indices on DRUG and REAC to speed up merging.
sqlite3 faers.db "CREATE INDEX drug_idx ON DRUG (ISR, DRUGNAME)"
sqlite3 faers.db "CREATE INDEX reac_idx ON REAC (ISR, PT)"

# Create DRUG_EVENT_COUNT table and remove duplicate records by grouping on ISR, DRUGNAME, PT
sqlite3 faers.db "CREATE TABLE DRUG_EVENT_COUNT AS SELECT DRUGNAME, PT, COUNT(DISTINCT(ISR)) AS COUNT FROM (SELECT ISR, DRUGNAME, PT FROM DRUG INNER JOIN REAC USING (ISR) WHERE DRUG.ISR IN (SELECT ISR FROM DEMO WHERE REPORTER_COUNTRY = 'UNITED STATES') GROUP BY ISR, PT, DRUGNAME) GROUP BY DRUGNAME, PT;"
sqlite3 faers.db "CREATE INDEX DRUG_EVENT_IDX ON DRUG_EVENT_COUNT (PT, DRUGNAME)"

# Clean up files.
find -name *TXT -exec rm {} \;
rm -rf ./data/sgml
rm -rf ./data/sqml
rm ./data/README.doc
