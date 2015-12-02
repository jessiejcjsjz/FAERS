#!/usr/bin/python
import Levenshtein
import operator

def create_drug_dicitonary(filename):
  """ This function creates a drug dictionary of the form
      {"synonym1":"generic1", "synonym2":"generic1"} using
      drug names (brand, generic, synonyms) found in DrugBank.
  """
  import csv 

  f = csv.reader(open(filename, 'rb'), delimiter="\t")
  drug_dictionary = {}

  for i in f:
    if i[0] == "WID": continue
    drug_dictionary[i[2].upper()] = i[2].upper()
    drug_dictionary[i[3].upper()] = i[2].upper()
    drug_dictionary[i[4].upper()] = i[2].upper()

  return drug_dictionary

def find_closest_string(query, dictionary, thresh=0.90):
  """ This function returns the closest match for 
      a query string against a dictionary of terms
      using levenstein distance
  """
  dist = {i:Levenshtein.jaro_winkler(query, i) for i in dictionary}
  dist = sorted(dist.items(), key=operator.itemgetter(1), reverse=True)
  if dist[0][1] >= thresh:
    return dist[0][0]
  else:
    return None

def harmonize(druglist, drugdict=False, thresh=0.90):
  """ This function takes a list of drugs (brand name,
      misspelled drugs, generic names) and converts them
      to the generic names. It is used to provide naming
      consistency to the FAERS reports.
  """
  if not drugdict:
    import pickle
    drugdict = pickle.load(open("drugs.pkl", "rb"))
 
  harmonized_druglist = []

  for drug in druglist:
    drug = drug.upper()
    gen = drugdict.get(drug)
    if gen:
      harmonized_druglist.append(gen)
      continue
    else:
      close_match = find_closest_string(drug, drugdict.keys(), thresh=thresh)
      close_match = drugdict.get(close_match)
      harmonized_druglist.append(close_match)

  return harmonized_druglist