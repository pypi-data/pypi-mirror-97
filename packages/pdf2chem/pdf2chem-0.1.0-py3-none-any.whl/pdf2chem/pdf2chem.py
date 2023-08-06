curation_type = "Exhaustive (includes 3-letter words)"

"""# Imports"""

# pip install chemdataextractor
import chemdataextractor as cde
#!cde data download

# pip install cirpy
import cirpy
import time

import re
import pandas as pd
import os
# pip install textract
import textract

from datetime import datetime

if curation_type == "Regular (ignores 3-letter words)":
  regex_number = 4
else:
  regex_number = 3

pdf_path = os.getcwd()

import sys
IN_COLAB = "google.colab" in sys.modules

if IN_COLAB:
  pdf_method = "pdfminer"
else:
  pdf_method = "pdftotext"

print("We\'ll use {} as the pdf extraction method.".format(pdf_method))

element_symbols = ['h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p', 's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga', 'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd', 'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'pm', 'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w', 're', 'os', 'ir', 'pt', 'au', 'hg', 'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th', 'pa', 'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'rf', 'db', 'sg', 'bh', 'hs', 'mt', 'ds ', 'rg ', 'cn ', 'nh', 'fl', 'mc', 'lv', 'ts', 'og']

false_positives = ['reno', 'lower', 'format', 'lead', 'nci', 'cc', 'isi', 'doi', "\\'b", 'is', 'ph', 'mv', 'zone', 'based', 'on', 'final', 'kato', 'cm', 'life', 'versus', 'www', 'can', 'ate', 'mm', 'crystal', 'sem', 'an', 's1', 'force', 'may', 'any', 'lau', 'voltage', 'kc', 'mino', 'm. h.', 'set', 'selective', 'c.p.k.', 'same', 'page 10', 'm-1', 'ai', 'c1', 'm2', 'et', 'fulfill', 'dry', 'via', 'may', 'pka', 'any', 'edge', 'b.v.', 'final', 'rt', '2b', 'h.y.', 'y.k.', 'v.v.', 'w.y.', 'good', 'region', 'cycle', 'des', 'force', 'may', 'dsc', 'chcl', 'counter', 'van', 'see', 'best', 'green', 'equal', 'result', 'challenge', 'substance', 'spectrum', 'der', 'its', 'glass', 'all', 'new', 'mix', 'so', 'soc.', 'arm', 'nm', 'ran', 'enable', 'sd', 'saa', 'map', 'ac1', 'fab', 'act', 'b7', 'liu', 'check', 'dual', 'via', 'den', 'fc', 'if', 'rapid', 'san', 'van', 'control', 'see', 'harry', 'adam', 'line', 'ac-1', 'sig', 'recruit', 'bli', 'test', 'tau', 'acs', 'iap', 'box', 'campaign', 'target', 'gfp', 'new', 'cv', 'rt', 'lid', 'compound', 'selective', 'rfb', 'ment', 'est', 'mm', 'con', 'con-', 's4', 'harry', 'ip', 'lp', 'ple', 'ml', 'prone', 'pka', 'sum', 'derivative', 'ten', 'min', 'vortex', 'gradual', 'tot', 'ber', 'red', 'ing', 'para', 'phs', 'gen', 'dft', 'nals', 'enable', 'set', 'versus', 'ma', 'the', 'and', 'eo', 'cps', 'ep', 'are', 'same', 'cos', 'age', 'sem', 's4', 'cycle', 'far', 'cal', 'overall', 'net', 'et', 'ml', 's1', 'prone', 'capture', 'or', 'rise', 'but', 'diurnal', 'dry', 'may', 'of', 'off', 'dp', 'if', 'dants', 'van', 'eden', 'line', 'tx', 'top', 'va', 'per', 'ny', 'on', 'ing', 'cp', 'for', 'dc', 'air', 'nhe', 'gas', 'zonal', 'all', 'new', 'based', 'had', 'ph', 'cm3', 'pyrite', 'soc', 'ser', 'acc', 'res', 'eds', 'mp', 'pro', 'inc', 'im', 'bv', 'disodium', 'ab', 'ed', 'carboxylate', '1mm', 'nat', 'eq', 'acc', 'sci', 'mol', 'int', 'sc-s', 'scs', 'gu', 'atm', 'shi', '2az', 'abbott', 'ms', 'wang', 'pdc', 'franklin', 'bay', 'dess', 'hbd', 'retard', 'intercept', 'iii', 'acid', 'fraction', 'aldrich', 'triton', 'cda', 'cyano', 'vinyl', 'flux', 'ethyl', 'methyl', 'mit', 'trigger', 'accelerate', 'ants', 'pentyl', 'laser', 'india', 'dos', 'los', 'acetyl', 'dec', 'sheets', 'tem', 'dimethyl', 'serial', 'tag', 'tandem', 'trap', 'mic', 'exciton', 'aldehyde', 'combat', 'roi', 'probiotic', 'antiviral', 'cada', 'beam', 'austin', 'lactone', 'lumen', 'diethyl', 'optimal', 'sulfoxide', 'gm3', 'gel', 'blockade', 'omega', 'cubes', 'bin', 'alcohols', 'alcohol', 'benchmark', 'portal', 'matrix', 'apex', 'bacterial', 'cube', 'linker', 'cascade', 'optimum', 'carbonyl oxygen', 'facet', 'shield']

if regex_number == 3:
  false_positives = [word for word in false_positives if not re.search("[a-zA-Z0-9+-]{3}", word) or re.search("[a-zA-Z0-9+-]{4}", word)]

"""# Define functions"""

def print_4():
  print('4')

def quick_curate(pdf_path, pdf_method, false_positives, regex_number):
#def quick_curate():

  """
  docstring coming soon
  """

  # extract the text from the pdf
  # the pdf_method should adapt to both local and hosted runtime compatibility
  text = textract.process(pdf_path, method=pdf_method)

  # queue up and reset list used to process the paper
  temp_word_list = []

  # strip new line and other markup from pdf mining
  text = str(text).replace("\\n-", '').replace('\-\n', '').replace('\-\n-', '').replace('\\n', ' ').replace('\n', ' ').replace('.', '')
  text = str(text).replace('*', "").replace('ISSN', '').replace('NSF', '').replace('NIH', '').replace("b'", '').replace(r"\r", '')

  # split by white spaces
  temp_word_list = re.split("\s+", str(text))

  # try to remove reference section by cutting off everything after the last mention of reference
  ref = [i for i, w in enumerate(temp_word_list) if w.lower().startswith('reference')]
  #print(ref)
  try:
    temp_word_list = temp_word_list[:(ref[-1])]
  except:
    pass

  # reconnect any words that got hyphenated and cut off at the end of a column
  for i, word in enumerate(temp_word_list):
    if re.search('[-]+$', word):
      temp_word_list[i] = word.replace('-', '') + temp_word_list[i+1]
      del(temp_word_list[i+1])

  print('The initial list for {} has {} words.'.format(pdf_path, len(temp_word_list)))

  # reconstruct a text string from the cleaned list; cde's NLP works on strings
  cleaned_text = ''
  for word in temp_word_list:
    cleaned_text += word
    cleaned_text += ' '

  # have cde do NLP on the string and convert the results into a list of strings
  doc = cde.Document(cleaned_text)
  chemicals_all = [span for span in doc.cems]
  chem_strings = [str(word).lower().replace('\n', ' ') for word in chemicals_all]

  # remove any blanks or null values
  chem_strings = [word for word in chem_strings if word]

  # remove anything left with a backslash in it
  chem_strings = [word for word in chem_strings if not re.search('[\\\+]', word)]

  print('We\'ll attempt to resolve {} potential chemicals.'.format(len(chem_strings)))

  # reset lists used for processing query hits and misses
  smiles_list = []
  already_queried = []
  missed_items = []

  for item in chem_strings:

    # if Sn is found, it's probably tin, not S=C
    if item.lower() == "sn":
      smiles_list.append('SnH4')
      print(item, smiles_list[-1])
      continue

    # keeping element symbols, such as H, C, or Na
    # this may turn into an option
    if item in element_symbols:
      smiles_list.append(cirpy.resolve(item, 'smiles'))
      print(item, smiles_list[-1])
      continue

    # adapt the regex code that leaves out short words/abbreviations to the user input above
    if regex_number == 4:

      if not re.search("[a-zA-Z0-9+-]{4}", item):
        smiles_list.append(None)
        print('Found a word that\'s a likely false positive: {}'.format(item))
        missed_items.append(item)
        continue

    if regex_number == 3:

      if not re.search("[a-zA-Z0-9+-]{3}", item):
        smiles_list.append(None)
        print('Found a word that\'s a likely false positive: {}'.format(item))
        missed_items.append(item)
        continue

    # save time by not querying chemicals that are in the text many times
    if item in already_queried:
      smiles_list.append(None)
      print('We\'ve already queried this one: {}'.format(item))

    # don't query the chemical if it's a known false positive
    # these include author names and a few other odds and ends
    elif item.strip('.').strip(',').lower() in false_positives:
      smiles_list.append(None)
      print('Found one known to be a false positive: {}'.format(item))

    # if the item passes all the tests, attempt to resolve it via NIH's CIR
    else:
      try:
          smiles_list.append(cirpy.resolve(item, 'smiles'))
          print(item, smiles_list[-1])
          time.sleep(0.21)

      # except loop in here to account for internet stability issues and the like
      except:
          try:
            print('Exception raised.  Pausing for 2 seconds and trying again')
            time.sleep(2)
            smiles_list.append(cirpy.resolve(item, 'smiles'))
            print(smiles_list[-1])
          except:
            try:
              print('Exception raised.  Pausing for another 2 seconds and trying again')
              time.sleep(2)
              smiles_list.append(cirpy.resolve(item, 'smiles'))
              print(smiles_list[-1])
            except:
              try:
                print('Exception raised.  Pausing for one more stretch and trying again')
                time.sleep(2)
                smiles_list.append(cirpy.resolve(item, 'smiles'))
                print(smiles_list[-1])
              except:
                print('It still raised an exception.  Here\'s how far it got:')
                print(smiles_list)
                print(len(smiles_list))
                print('This item will be added to a list called missed items.')
                print(item)
                smiles_list.append('Check')
                missed_items.append(item)
    already_queried.append(item)

  # tidy these up into pandas dataframes and export them as csv files
  chem_df = pd.DataFrame(zip(chem_strings, smiles_list), columns=('Name', 'SMILES'))
  chem_df = chem_df.dropna()
  chem_df.to_csv(os.path.splitext(pdf_path)[0]+'_'+datetime.today().strftime('%Y%m%d')+'_names_and_SMILES.csv')
  if missed_items:
    missed_df = pd.DataFrame(missed_items, columns=['Missed'])
    missed_df = missed_df.drop_duplicates()
    missed_df.to_csv(os.path.splitext(pdf_path)[0]+'_'+datetime.today().strftime('%Y%m%d')+'_zzz_missed_items.csv')

  # return chem_df

def aggregate_csv_files():
  # combines all results files into a single csv file
  all_chemicals = pd.concat([pd.read_csv(filename) for filename in os.listdir(pdf_dir) if re.search('csv$', filename)])
  all_chemicals.to_csv(datetime.today().strftime('%Y%m%d')+"combined_csv.csv", index=False, encoding='utf-8-sig')

"""# Curate pdfs"""

#@title ## Curator output will appear below
def curate_folder():
  pdf_dir = os.getcwd()

  pd.DataFrame(data=None, columns=('Name', 'SMILES'))

  assert os.path.exists(pdf_dir), "I did not find the directory at, "+str(pdf_dir)

  os.chdir(pdf_dir)

  for filename in os.listdir(pdf_dir):
    if re.search('pdf$', filename):
      try:
        chemicals = quick_curate(filename, pdf_method, false_positives, regex_number)
      except:
        print('An exception was raised for ' + filename)
        print('Most likely, an error occurred when trying to extract text from the pdf.')

  try:
    aggregate_csv_files()
  except:
    "An error occurred while trying to combine the output csv files."
