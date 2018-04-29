#!/usr/bin/env python3

import argparse
import csv
import re
from tabulate import tabulate
import xml.etree.ElementTree

ignore_aliases = [
        "Stichting",
        '.',
        '',
        'verzender',
        'Verzender',
]

def fetch_anbi_list():
    e = xml.etree.ElementTree.parse('anbi.xml').getroot()
    names = []
    for beschikking in e.findall('beschikking'):
        einddatum = beschikking.find('eindDatum')
        aliasnaam = beschikking.find('aliasNaam')
        if einddatum is not None:
            year = einddatum.text[0:4]
            if einddatum != '2017':
                continue
        naam = beschikking.find('naam').text
        if aliasnaam is not None:
            aliasnaam = aliasnaam.text
        names.append({'naam': naam, 'alias': aliasnaam})
    return names

def parse_csv(filename):
    transacties = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            values = list(row.values())
            verzender = values[3]
            euros = float(values[7])
            beschrijving = values[11]
            transacties.append({
                'verzender': verzender,
                'euros':  euros,
                'beschrijving': beschrijving
                })
    return transacties

def valid_alias(alias):
    trimmed_alias = alias.strip() if alias is not None else ''
    if trimmed_alias is not None and len(trimmed_alias) > 4 and trimmed_alias not in ignore_aliases:
        return True
    return False

def string_found(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False

def find_anbis(csv_file):
    names = fetch_anbi_list()
    found = []
    betalingen = parse_csv(csv_file)
    for anbi in names:
        for betaling in betalingen:
            if anbi['naam'] in betaling['beschrijving']:
                found.append({'naam': betaling['verzender'], 'bedrag': betaling['euros']})
            elif anbi['naam'] in betaling['verzender']:
                found.append({'naam': betaling['verzender'], 'bedrag': betaling['euros']})
            elif valid_alias(anbi['alias']) and string_found(anbi['alias'],  betaling['beschrijving']):
                found.append({'naam': betaling['verzender'], 'bedrag': betaling['euros']})
            elif valid_alias(anbi['alias']) and string_found(anbi['alias'], betaling['verzender']):
                found.append({'naam': betaling['verzender'], 'bedrag': betaling['euros']})
    return found

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="CSV of your transaction")
    args = parser.parse_args()
    found = find_anbis(args.csv)
    print(tabulate(found, tablefmt="grid", headers='keys'))
main()
