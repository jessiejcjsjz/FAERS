#!/usr/bin/python

import pandas as pd
import sqlite3
import sys

# Create SQLite connection
con = sqlite3.connect("./faers.db")

# Define columns to keep
drug_columns = [u'primaryid', u'caseid', u'drug_seq', u'role_cod', u'drugname', u'val_vbm', u'route', u'dose_vbm', u'cum_dose_chr', u'cum_dose_unit', u'dechal', u'rechal', u'lot_num', u'exp_dt', u'nda_num', u'dose_amt', u'dose_unit', u'dose_form', u'dose_freq']
demo_columns = [u'primaryid', u'caseid', u'caseversion', u'i_f_code', u'event_dt', u'mfr_dt', u'init_fda_dt', u'fda_dt', u'rept_cod', u'mfr_num', u'mfr_sndr', u'age', u'age_cod', u'e_sub', u'wt', u'wt_cod', u'rept_dt', u'to_mfr', u'occp_cod', u'reporter_country', u'occr_country']
indi_columns = [u'primaryid', u'caseid', u'indi_drug_seq', u'indi_pt']
outc_columns = [u'primaryid', u'caseid', u'outc_cod']
reac_columns = [u'primaryid', u'caseid', u'pt']
rpsr_columns = [u'primaryid', u'caseid', u'rpsr_cod']
ther_columns = [u'primaryid', u'caseid', u'start_dt', u'end_dt', u'dur', u'dur_cod']

# Function for standardizing date names to yyyymmdd format
def to_date(x):
    s = str(x).replace(".0", "")
    if len(s) == 8: s = s
    if len(s) == 6: s =  s + "01"
    if len(s) == 4: s = s + "0101"
    try:
        return pd.to_datetime(s, format='%Y%m%d')
    except:
        return ""
    
# Load data into appropriate SQLite table
def import_data(filename):
    if "DRUG" in filename:
        drug = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        drug[drug_columns].to_sql("drug", con, if_exists="append")

    if "DEMO" in filename:
        demo = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        demo['event_dt'] = demo['event_dt'].apply(to_date).astype(str)
        demo['mfr_dt'] = demo['mfr_dt'].apply(to_date).astype(str)
        demo['rept_dt'] = demo['rept_dt'].apply(to_date).astype(str)
        demo['to_mfr'] = demo['to_mfr'].apply(to_date).astype(str)
        demo['init_fda_dt'] = demo['init_fda_dt'].apply(to_date).astype(str)
        demo['fda_dt'] = demo['fda_dt'].apply(to_date).astype(str)
        demo[demo_columns].to_sql("demo", con, if_exists="append")

    if "INDI" in filename:
        indi = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        indi[indi_columns].to_sql("indi", con, if_exists="append")

    if "OUTC" in filename:
        outc = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        outc[outc_columns].to_sql("outc", con, if_exists="append")

    if "REAC" in filename:
        reac = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        reac[reac_columns].to_sql("reac", con, if_exists="append")

    if "RPSR" in filename:
        rpsr = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        rpsr[rpsr_columns].to_sql("rpsr", con, if_exists="append")

    if "THER" in filename:
        ther = pd.read_csv(filename, sep="$", encoding='utf-8', low_memory=False)
        ther[ther_columns].to_sql('ther', con, if_exists='append')

import_data(sys.argv[1])
