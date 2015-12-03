def proportional_reporting_ratio(drug, event, db):
    n = int(db.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME LIKE '%s' AND PT LIKE '%s'" % (drug, event)).fetchone()[0])
    m = float(db.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME LIKE '%s' AND PT NOT LIKE '%s'" % (drug, event)).fetchone()[0])
    p = int(db.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME NOT LIKE '%s' AND PT LIKE '%s'" % (drug, event)).fetchone()[0])
    q = float(db.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME NOT LIKE '%s' AND PT NOT LIKE '%s'" % (drug, event)).fetchone()[0])
    return (n/m) / (p/q)
