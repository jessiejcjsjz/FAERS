#!/bin/bash
sqlite3 faers.cp "CREATE INDEX drug_idx ON DRUG (ISR, DRUGNAME)"
sqlite3 faers.cp "CREATE INDEX reac_idx ON REAC (ISR, PT)"
