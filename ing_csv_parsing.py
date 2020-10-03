import csv
from collections import namedtuple
import re


CategoryMapping = namedtuple("CategoryMapper", "keyword category")
PaymentEntry = namedtuple("PaymentEntry", "date name destination source code in_out amount")

CATEGORIES = [
CategoryMapping("Lidl","Groceries"),
CategoryMapping("KFC","Fast Food"),
CategoryMapping("WEBB","Salary"),
CategoryMapping("Jumbo","Groceries"),
CategoryMapping("Action","Household"),
CategoryMapping("Kruidvat","Household"),
CategoryMapping("OXXIO","Utilities"),
CategoryMapping("hypotheken","Mortgage"),
CategoryMapping("VvE Venserpolder","Utilities"),
CategoryMapping("AnderZorg","Insurance"),
CategoryMapping("Moneybookers","Credit card Skrill"),
CategoryMapping("TIKKIE","Tikkies"),
CategoryMapping("T-MOBILE","Utilities"),
CategoryMapping("Feiken","Utilities"),
CategoryMapping("SIMYO","Utilities"),
CategoryMapping("V Munteanu","Investments"),
CategoryMapping("SHELL","Gas"),
CategoryMapping("BasisPakket","Utilities"),
CategoryMapping("CCV*","Restaurants"),
CategoryMapping("Erno s","Restaurants"),
CategoryMapping("SWDA","Restaurants"),
CategoryMapping("Rabo Betaalverzoek","Tikkies"),
CategoryMapping("ABN AMRO Bank NV","Tikkies"),
CategoryMapping("NZV","Restaurants"),
CategoryMapping("ENNL","ATM"),
CategoryMapping("Simz","Restaurants"),
CategoryMapping("Toko","Restaurants"),
CategoryMapping("ATM","ATM"),
CategoryMapping("VanderBoom","Clothes"),
CategoryMapping("Scooter","Scooter"),
CategoryMapping("Ticket","Tickets"),
CategoryMapping("BK","Fast Food"),
CategoryMapping("Molnar","Molnar"),
CategoryMapping("GHEORGHE","Andreea"),
CategoryMapping("van Veen","Jeroen"),
CategoryMapping("PRAXIS","Household"),
CategoryMapping("SCHOOL OF LIFE","Restaurants"),
CategoryMapping("Multisafe","Salsa"),
CategoryMapping("Hasta la Pasta","Restaurants"),
CategoryMapping("KATSU","Restaurants"),
CategoryMapping("Belastingdienst","Taxes"),
CategoryMapping("Eventbrite","Tickets"),
CategoryMapping("Jaap Edenbaan","Restaurants"),
CategoryMapping("Waternet","Utilities"),
CategoryMapping("C&M","Clothes"),
CategoryMapping("Spotify","Online serv"),
CategoryMapping("Amazon","Online serv"),
CategoryMapping("Bol","Online serv"),
CategoryMapping("ETOS","Household"),
CategoryMapping("Gall & Gall","Groceries"),
CategoryMapping("RegioBank","Tikkies"),
CategoryMapping("Salsa Shop","Restaurants"),
CategoryMapping("Cafe De IJsbreker","Restaurants"),
CategoryMapping("Lil Cities","Restaurants"),
CategoryMapping("Cabron","Restaurants"),
CategoryMapping("Marmaris","Restaurants"),
CategoryMapping("Alipay","Online serv"),
CategoryMapping("Verzekeren","Insurance"),
CategoryMapping("Betaalverzoek","Tikkies"),
CategoryMapping("ALBERT HEIJN","Groceries"),
CategoryMapping("Waterschap","Taxes"),
CategoryMapping("BLOKKER","Household"),
CategoryMapping("Gamma","Household"),
CategoryMapping("PYVLios","Restaurants"),
CategoryMapping("CALIFORNIA BURRITO","Restaurants"),
CategoryMapping("Pathe ","Tickets"),
CategoryMapping("IWAB","Online serv"),
CategoryMapping("belastingen","Taxes"),
CategoryMapping("Kleuro","Online serv"),
CategoryMapping("IKEA","Household"),
CategoryMapping("Dominos","Fast Food"),
CategoryMapping("Cafe Mez","Restaurants"),
CategoryMapping("Gall Gall","Groceries"),
CategoryMapping("NSAdam","tickets"),
CategoryMapping("ZEEMAN","Household"),
CategoryMapping("MACHADO","Mortgage"),
CategoryMapping("SPYLunch","Restaurants"),
CategoryMapping("vanHaren","Clothes"),
CategoryMapping("SumUp","Restaurants"),
CategoryMapping("Bijlmerplein","Restaurants")
]



def parse_csv(filename):
    with open(filename, 'r') as csvfile:
        transactions = csv.reader(csvfile, delimiter=',', quotechar='"')

        # skip the first row
        next(transactions)

        entries = []

        for row in transactions:
            entries.append(PaymentEntry(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return entries

def process_entries(entries):
    result = {"not_found": 0.0}


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
            # result["not_found"] +=float(row[6].replace(",","."))
            print(row)

    print("++++++")
    print(result)
    return result