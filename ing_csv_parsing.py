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


def add_missing_category(dict, month, category):
    if month not in dict:
        dict[month] = {}
    if category not in dict[month]:
        dict[month][category] = 0

def process_entries(entries, mapping_entries):
    result_income = { "Other Incomes" : 0.0}
    result_expenses = {"Other Expenses": 0.0}

    not_mapped_entries = []

    for row in entries:
        found = False
        month = row.date[0:6]
        month = f"{month[:4]}-{month[4:]}"
        for mapping in mapping_entries:
            if re.search(mapping.keyword, row.name, re.IGNORECASE):
                found = True
                amount = float(row.amount.replace(",", "."))
                if row.in_out == "Af":
                    add_missing_category(result_expenses, month, mapping.category)
                    result_expenses[month][mapping.category] += amount
                else:
                    add_missing_category(result_income, month, mapping.category)
                    result_income[month][mapping.category] += amount
        if not found:
            try:
                value = float(row[6].replace(",", "."))
                if row.in_out == "Af":
                    add_missing_category(result_expenses, month, "Other Expenses")
                    result_expenses[month]["Other Expenses"] -= value
                else:
                    add_missing_category(result_income, month, "Other Incomes")
                    result_income[month]["Other Incomes"] += value
            except:
                logging().error("Field" + row.amount + " not a number")
            not_mapped_entries.append(row.name)
            print(row)

    if result_expenses["Other Expenses"]  == 0.0:
        del result_expenses["Other Expenses"]

    if result_income["Other Incomes"] == 0.0:
        del result_income["Other Incomes"]

    print(result_income)
    print(result_expenses)
    return result_income, result_expenses, set(not_mapped_entries)