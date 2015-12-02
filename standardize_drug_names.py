#!/usr/bin/python

import drug_name_standardizer as ds
import sqlite3
THRESH = 0.95
conn = sqlite3.connect("faers.db")
curs = conn.cursor()

faers_unique_drug_list = [i[0] for i in curs.execute("SELECT DISTINCT(DRUGNAME) FROM DRUG").fetchall()]
standardized_drug_list = ds.standardize(faers_unique_drug_list, thresh=THRESH)

for i in range(len(faers_unique_drug_list)):
    original = faers_unique_drug_list[i]
    replacement = standardized_drug_list[i]
    if original != replacement and replacement != None:
        sql = "UPDATE DRUG SET DRUGNAME = " + replacement + " WHERE DRUGNAME = " + original
        curs.execte(sql)
        curs.commit()
        print "%s ==> %s" % (original, replacement)
