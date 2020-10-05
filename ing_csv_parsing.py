import csv
from collections import namedtuple
import re
import logging

CategoryMapping = namedtuple("CategoryMapper", "keyword category")
PaymentEntry = namedtuple("PaymentEntry", "date name destination source code in_out amount")

def read_category_mappings(filename):
    with open(filename, 'r') as csvfile:
        mappings = csv.reader(csvfile, delimiter=',', quotechar='"')

        # skip the first row
        next(mappings)

        mapping_entries = []

        for row in mappings:
            mapping_entries.append(CategoryMapping(row[0], row[1]))

        return mapping_entries


def parse_csv(filename, mapping_entries):
    with open(filename, 'r') as csvfile:
        transactions = csv.reader(csvfile, delimiter=',', quotechar='"')

        # skip the first row
        next(transactions)

        entries = []

        for row in transactions:
            entries.append(PaymentEntry(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return entries

def process_entries(entries):
    result = {"Other Expenses": 0.0}

    not_mapped_entries = []


    for row in entries:

        found = False
        for mapping in CATEGORIES:
            if re.search(mapping.keyword, row.name, re.IGNORECASE):
                found = True
                if mapping.category not in result:
                    result[mapping.category] = 0.0
                amount = float(row.amount.replace(",", "."))
                if row.in_out == "Af":
                    result[mapping.category] -= amount
                else:
                    result[mapping.category] += amount
        if not found:
            try:
                result["Other Expenses"] +=float(row[6].replace(",","."))
            except:
                logging().error("Field" + row.amount + " not a number")
            print(row)

    print("++++++")
    print(result)
    return result