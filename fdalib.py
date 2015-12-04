import sqlite3
import drugstandards as drugs

class FAERS:
    def __init__(self, filename):
        """ This method is used to establish a connection 
            with an existing FAERS database.
        """
        self.conn = sqlite3.connect(filename)
        
    def proportional_reporting_ratio(self, drug, event):
        """ This method will return the proportional-reporting-ratio (PRR)
            for a given drug-reaction pair.
        """
        drug = drugs.standardize([drug])[0]
        event = event.upper()
        n = int(self.conn.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME LIKE '%%%s%%' AND PT LIKE '%%%s%%'" % (drug, event)).fetchone()[0])
        m = float(self.conn.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME LIKE '%%%s%%'" % drug).fetchone()[0])
        p = int(self.conn.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME NOT LIKE '%%%s%%' AND PT LIKE '%%%s%%'" % (drug, event)).fetchone()[0])
        q = float(self.conn.execute("SELECT COUNT(*) FROM EVENT WHERE DRUGNAME NOT LIKE '%%%s%%'" % drug).fetchone()[0])
        sim_drug_terms = self.conn.execute("SELECT DRUGNAME FROM EVENT WHERE DRUGNAME LIKE '%%%s%%' GROUP BY DRUGNAME" % drug).fetchall()
        sim_event_terms = self.conn.execute("SELECT PT FROM EVENT WHERE PT LIKE '%%%s%%' GROUP BY PT" % event).fetchall()
        sim_drug_terms = [i[0] for i in sim_drug_terms]
        sim_event_terms = [i[0] for i in sim_event_terms]
        print "PRR ""calculated using (" + " OR ".join(sim_drug_terms) + ") AND (" + " OR ".join(sim_event_terms) + ")"""
        return (n/m) / (p/q)

    def drug_event_stats(self, drug, event):
        """ This metho computes frequencies used in calculating the PRR:
            Freq event | drug: the frequency that event is found with drug.
            Freq anyevent | drug: the frequency that any event is associated with drug.
            Freq event | other drugs: the frequency that the event is observed with all other drugs.
            Freq anyevent | other drugs: the frequnecy that any event is assciated with all other drugs.
        """
        event_drug = "SELECT SUM(COUNT) FROM DRUG_EVENT_COUNT WHERE DRUGNAME LIKE '%%%s%%' AND PT LIKE '%%%s%%'" % (drug, event)
        anyevent_drug = "SELECT SUM(COUNT) FROM DRUG_EVENT_COUNT WHERE DRUGNAME LIKE '%%%s%%'" % (drug)
        event_otherdrugs = "SELECT SUM(COUNT) FROM DRUG_EVENT_COUNT WHERE DRUGNAME NOT LIKE '%%%s%%' AND PT LIKE '%%%s%%'" % (drug, event)
        anyevent_otherdrugs = "SELECT SUM(COUNT) FROM DRUG_EVENT_COUNT WHERE DRUGNAME NOT LIKE '%%%s%%'" % (drug)
        event_drug = self.conn.execute(event_drug).fetchone()[0]
        anyevent_drug = self.conn.execute(anyevent_drug).fetchone()[0]
        event_otherdrugs = self.conn.execute(event_otherdrugs).fetchone()[0]
        anyevent_otherdrugs = self.conn.execute(anyevent_otherdrugs).fetchone()[0]
        return {"event_drug":event_drug, "anyevent_drug":anyevent_drug, "event_otherdrugs":event_otherdrugs, "anyevent_otherdrugs":anyevent_otherdrugs}

    def prr(self, drug, event):
        drug = drugs.standardize([drug])[0]
        event = event.upper()
        result = self.drug_event_stats(drug, event)
        prr = (result["event_drug"]/float(result["anyevent_drug"])) / (result["event_otherdrugs"]/float(result["anyevent_otherdrugs"]))
        return prr

    def common_events(self, drugname, sortby="COUNT"):
        """ This method will return a sorted list of drug-event frequencies.
        """
        drugname = drugs.standardize([drugname])[0]
        sql = "SELECT DRUGNAME, PT, COUNT(*) AS COUNT FROM EVENT WHERE DRUGNAME = '%s' GROUP BY DRUGNAME, PT ORDER BY %s DESC" % (drugname.upper(), sortby)
        results = self.conn.execute(sql).fetchall()
        return [[str(k),str(v),c] for k,v,c in results]

    def drug_counts(self, sortby="COUNT"):
        """ This method will return a sorted list of drug frequencies.
        """
        sql = "SELECT DRUGNAME, COUNT(*) AS COUNT FROM EVENT GROUP BY DRUGNAME ORDER BY %s DESC" % sortby
        results = self.conn.execute(sql).fetchall()
        return results
        print len(results)
        print len(results[0])
        return [[str(k),v] for k,v,m in results]

    def event_counts(self, sortby="COUNT"):
        """ This method wil return a sorted list of event frequencies.
        """
        sql = "SELECT PT AS EVENT, COUNT(*) AS COUNT FROM EVENT GROUP BY PT ORDER BY %s DESC" % sortby
        results = self.conn.execute(sql).fetchall()
        return [[str(k),v] for k,v in results]

    def find_like_drugs(self, drug, sortby="COUNT"):
        """ Return a list of all similar drug names.
        """
        sql = "SELECT DRUGNAME, COUNT(*) AS COUNT FROM EVENT WHERE DRUGNAME LIKE '%%" + drug.upper() + "%%' GROUP BY DRUGNAME ORDER BY %s DESC" % sortby
        results = self.conn.execute(sql).fetchall()
        return [[str(k),v] for k,v in results]
