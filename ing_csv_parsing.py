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
            mapping_entries.append(CategoryMapping(row[0].strip(), row[1].strip()))

        return mapping_entries


def parse_csv(filename):
    with open(filename, 'r') as csvfile:
        transactions = csv.reader(csvfile, delimiter=',', quotechar='"')

        # skip the first row
        next(transactions)

        entries = []

        for row in transactions:
            entries.append(PaymentEntry(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return entries

def process_entries(entries, mapping_entries):
    result_income = { "Other Incomes" : 0.0}
    result_expenses = {"Other Expenses": 0.0}

    not_mapped_entries = []


    for row in entries:

        found = False
        for mapping in mapping_entries:
            if re.search(mapping.keyword, row.name, re.IGNORECASE):
                found = True
                amount = float(row.amount.replace(",", "."))
                if row.in_out == "Af":
                    if mapping.category not in result_expenses:
                        result_expenses[mapping.category] = 0.0
                    result_expenses[mapping.category] += amount
                else:
                    if mapping.category not in result_income:
                        result_income[mapping.category] = 0.0
                    result_income[mapping.category] += amount
        if not found:
            try:
                value = float(row[6].replace(",", "."))
                if row.in_out == "Af":
                    result_expenses["Other Expenses"] -= value
                else:
                    result_income["Other Incomes"] += value
            except:
                logging().error("Field" + row.amount + " not a number")
            not_mapped_entries.append(row.name)
            print(row)

    print("++++++")
    if result_expenses["Other Expenses"]  == 0.0:
        del result_expenses["Other Expenses"]

    if result_income["Other Incomes"] == 0.0:
        del result_income["Other Incomes"]

    print(result_income)
    print(result_expenses)
    return result_income, result_expenses, set(not_mapped_entries)