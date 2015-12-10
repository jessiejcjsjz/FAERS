#!/bin/bash

# Create database schema.
DRUG="CREATE TABLE drugs (PRIMARYID INT, CASEID INT, DRUG_SEQ INT, ROLE_COD TEXT, DRUGNAME TEXT, VAL_VBM TEXT, ROUTE TEXT, DOSE_VBM TEXT, CUM_DOSE_CHR TEXT, CUM_DOS_UNIT TEXT, DECHAL TEXT, RECHAL TEXT, LOT_NUM TEXT, EXP_DT INT, NDA_NUM INT, DOSE_AMT TEXT, DOSE_UNIT TEXT, DOSE_FORM TEXT, DOSE_FREQ TEXT);"
DEMO="CREATE TABLE demos (PRIMARYID INT, CASEID INT, CASE_VERSION INT, IF_CODE TEXT, EVENT_DT INT, MFR_DT INT, INIT_FDA_DATE INT, FDA_DT INT, REPT_COD TEXT, MFR_NUM TEXT, MFR_SNDR TEXT, AGE INT, AGE_COD TEXT, GNDR_COD TEXT, E_SUB TEXT, WT INT, WT_COD TEXT, REPT_DT INT, TO_MFR TEXT, OCCP_COD TEXT, REPORTER_COUNTRY TEXT, OCCR_COUNTRY);"
INDI="CREATE TABLE indis (PRIMARYID INT, CASEID INT, INDI_DRUG_SEQ INT, INDI_PT TEXT);"
OUTC="CREATE TABLE outcs (PRIMARYID INT, CASEID INT, OUTC_COD TEXT);"
REAC="CREATE TABLE reacs (PRIMARYID INT, CASEID INT, PT TEXT);"
RPSR="CREATE TABLE rpsrs (PRIMARYID INT, CASEID INT, RPSR_COD TEXT);"
THER="CREATE TABLE thers (PRIMARYID INT, CASEID INT, DSG_DRUG_SEQ INT, START_DT INT, END_DT INT, DUR INT, DUR_COD TEXT);"

# Setup database schema
echo "Setting up schema..."
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
  unzip -o $filename -d data/
  echo "`date`: begninning import for $filename"
  echo "Importing DRUG table..."
  find data/ -iname DRUG*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' drugs"
  echo "Importing DEMO table..."
  find data/ -iname DEMO*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' demos"
  echo "Importing INDI table..."
  find data/ -iname INDI*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' indis"
  echo "Importing OUTC table..."
  find data/ -iname OUTC*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' outcs"
  echo "Importing REAC table..."
  find data/ -iname REAC*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' reacs"
  echo "Importing RPSR table..."
  find data/ -iname RPSR*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' rpsrs"
  echo "Importing THER table..."
  find data/ -iname THER*txt | xargs -I % sqlite3 faers.db -separator $ ".import '"%"' thers"

  # Clean up files.
  find data/ -name '*txt' -exec rm {} \;
  find data/ -name '*pdf' -exec rm {} \;
  find data/ -name '*doc' -exec rm {} \;
  rm -rf ./data/sgml
  rm -rf ./data/sqml
  rm -rf ./data/as*
  rm -rf ./data/ASCII
done;

# Delete header rows.
sqlite3 faers.db "DELETE FROM drugs WHERE PRIMARYID = 'primaryid'"
sqlite3 faers.db "DELETE FROM demos WHERE PRIMARYID = 'primaryid'"
sqlite3 faers.db "DELETE FROM indis WHERE PRIMARYID = 'primaryid'"
sqlite3 faers.db "DELETE FROM outcs WHERE PRIMARYID = 'primaryid'"
sqlite3 faers.db "DELETE FROM reacs WHERE PRIMARYID = 'primaryid'"
sqlite3 faers.db "DELETE FROM rpsrs WHERE PRIMARYID = 'primaryid'"
sqlite3 faers.db "DELETE FROM thers WHERE PRIMARYID = 'primaryid'"

# Remove duplicate rows from tables
sqlite3 faers.db "CREATE TABLE DRUG AS SELECT * FROM drugs GROUP BY PRIMARYID, DRUG_SEQ"
sqlite3 faers.db "CREATE TABLE DEMO AS SELECT * FROM demos GROUP BY PRIMARYID"
sqlite3 faers.db "CREATE TABLE INDI AS SELECT * FROM indis GROUP BY PRIMARYID, INDI_DRUG_SEQ, INDI_PT"
sqlite3 faers.db "CREATE TABLE OUTC AS SELECT * FROM outcs GROUP BY PRIMARYID, OUTC_COD"
sqlite3 faers.db "CREATE TABLE REAC AS SELECT * FROM reacs GROUP BY PRIMARYID, PT"
sqlite3 faers.db "CREATE TABLE RPSR AS SELECT * FROM rpsrs GROUP BY PRIMARYID, RPSR_COD"
sqlite3 faers.db "CREATE TABLE THER AS SELECT * FROM thers GROUP BY PRIMARYID, DSG_DRUG_SEQ"

# Remove old tables
sqlite3 faers.db "DROP TABLE drugs"
sqlite3 faers.db "DROP TABLE demos"
sqlite3 faers.db "DROP TABLE indis"
sqlite3 faers.db "DROP TABLE outcs"
sqlite3 faers.db "DROP TABLE reacs"
sqlite3 faers.db "DROP TABLE rpsrs"
sqlite3 faers.db "DROP TABLE thers"

# Create indisces on DRUG and REAC to speed up merging.
sqlite3 faers.db "CREATE INDEX drugs_idx ON DRUG (PRIMARYID, DRUGNAME)"
sqlite3 faers.db "CREATE INDEX reacs_idx ON REAC (PRIMARYID, PT)"
sqlite3 faers.db "CREATE INDEX demos_idx ON DEMO (REPORTER_COUNTRY, EVENT_DT)"
