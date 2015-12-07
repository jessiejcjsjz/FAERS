#!/usr/bin/python

import drugstandards as drugs
import sqlite3
import csv

# Set the minmal Jario-Winkler similarity required for two strings to be considered a match.
THRESH = 0.9

# Establish connection to faers database which was created by running ./import_faers_data.sh
conn = sqlite3.connect("faers.db")

# Get unique drug names from faers.db to standardize.
faers = [i[0] for i in conn.execute("SELECT DISTINCT(DRUGNAME) FROM DRUG").fetchall() if i[0] != None]

# Standardize drug names form above.
stand = drugs.standardize(faers, thresh=THRESH)
pairs = [ (faers[i], stand[i]) for i in range(len(stand)) if stand[i] != None and faers[i] != stand[i]]
print "Adding %d records to DRUG_MAP" % len(pairs)

# Add DRUG_MAP table.
conn.execute('CREATE TABLE DRUG_MAP (ORIGINAL TEXT, REPLACEMENT TEXT)')
conn.executemany('INSERT INTO DRUG_MAP (ORIGINAL, REPLACEMENT) VALUES (?, ?)', (pairs))
conn.execute('CREATE INDEX drug_map_idx ON DRUG_MAP (ORIGINAL, REPLACEMENT)')
conn.commit()
