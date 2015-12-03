#!/usr/bin/python

import drugstandards as drugs
import sqlite3
import csv

THRESH = 0.9

report = csv.writer(open("report_standardization.csv","wb"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
report.writerow(["ORIGINAL", "REPLACEMENT", "OCCURRENCE"])
conn = sqlite3.connect("faers.db")

# Generate drug count report prior to standardizing.
pre_counts = conn.execute("SELECT DRUGNAME, COUNT(DRUGNAME) FROM DRUG GROUP BY DRUGNAME").fetchall()
pre_counts_report = csv.writer(open("report_pre_standardization.csv", "wb"), delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
pre_counts_report.writerow(["TERM", "COUNT"])

for i in pre_counts:
    pre_counts_report.writerow([i[0], i[1]])

faers = [i[0] for i in conn.execute("SELECT DISTINCT(DRUGNAME) FROM DRUG").fetchall() if i[0] != None]
print "Got unique list: n = %d" % len(faers)
print "Standardizing drug names..."

stand = drugs.standardize(faers, thresh=THRESH)
print "Finished standardizing drug names..."
print "Updating table..."
pairs = [(stand[i], faers[i]) for i in range(len(stand)) if stand[i] != None and faers[i] != stand[i]]
for i in pairs:
    try:
        n = int(conn.execute("SELECT COUNT(*) FROM DRUG WHERE DRUGNAME = '%s'" % i[1]).fetchone()[0])
        print "Updating %s ==> %s : %d" % (i[1], i[0], n)
        report.writerow([i[1], i[0], n])
    except:
        pass

conn.executemany("UPDATE DRUG SET DRUGNAME = ? WHERE DRUGNAME = ?", pairs)
conn.commit()

# Generate drug count report after applying standardization.
post_std_counts = csv.writer(open("report_post_standardization.csv", "wb"))
post_counts = conn.execute("SELECT DRUGNAME, COUNT(DRUGNAME) FROM DRUG GROUP BY DRUGNAME").fetchall()


for i in post_counts:
    post_std_counts.writerow([i[0], i[1]])
    
