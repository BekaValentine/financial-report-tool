import csv
import json
import os
import sys
import time


class CategoryManager:

    def __init__(self):
        if not os.path.isfile('categories.json'):
            with open('categories.json', 'w') as f:
                f.write(json.dumps({}))

        with open('categories.json', 'r') as f:
            self.categories = json.loads(f.read())

    def save(self):
        with open('categories.json', 'w') as f:
            f.write(json.dumps(self.categories))

    def add_criterion(self, cat, criterion):
        if cat not in self.categories:
            self.categories[cat] = []

        self.categories[cat] += [criterion]

        self.save()

    def names(self):
        return self.categories.keys()

    def categorize(self, description):
        for cat, criteria in self.categories.items():
            for criterion in criteria:
                if criterion.lower() in description.lower():
                    return cat
        return None


class Table:
    def __init__(self, file_path):
        self.rows = []
        with open(file_path, 'r') as f:
            for row in csv.DictReader(f):
                self.rows += [Transaction.from_row(row)]


class Transaction:

    with open('table_settings.json', 'r') as f:
        settings = json.loads(f.read())

    @classmethod
    def from_row(cls, od_row):
        return Transaction(od_row[cls.settings['date']], float(od_row[cls.settings['amount']]), od_row[cls.settings['description']])

    def __init__(self, date, amount, description):
        self.date = date
        self.amount = amount
        self.description = description

    def pretty_print(self):
        return '  {date:<10}    ${amount:<10,.2f}    {description}'.format(date=self.date, amount=self.amount, description=self.description)


class Category:

    def __init__(self, name):
        self.name = name
        self.totalx100 = 0.0
        self.transactions = []

    def add_transaction(self, tx):
        self.totalx100 += 100 * tx.amount
        self.transactions += [tx]

    def total(self):
        return self.totalx100 / 100

    def pretty_print(self):
        lines = ['== {cat} / ${total:,.2f} =='.format(
            cat=self.name, total=self.totalx100 / 100),
            '']

        for tx in self.transactions:
            lines += [tx.pretty_print()]

        return '\n'.join(lines)


class Ledger:

    def __init__(self):
        self.categories = {}

    def add_transaction(self, cat_name, tx):
        if cat_name not in self.categories:
            self.categories[cat_name] = Category(cat_name)

        self.categories[cat_name].add_transaction(tx)

    def pretty_print(self):
        lines = []

        for cat in sorted(self.categories.keys()):
            category = self.categories[cat]
            lines += [category.pretty_print()]

        return '\n\n'.join(lines)


def get_categories(uncategorized, cat_mgr, ledger):
    while uncategorized:
        tx = uncategorized[0]
        print()
        print()
        print('The following transaction was uncategorized:')
        print()
        print(tx.pretty_print())
        print()

        names = cat_mgr.names()
        if names:
            print('What category should I add it to? You can give a new one, or select one of these existing ones:')
            print()
            print('  ' + ', '.join(cat_mgr.names()))
        else:
            print('What category should I add it to?')

        print()
        cat_name = input('  Selected category: ')

        print()
        print('What substring was used to identify this category from the description?')
        print()
        substr = input('  Substring: ')

        time.sleep(0.5)

        print()
        print('Ok. I shall add this transaction to the category ' +
              cat_name + ' because it contained ' + repr(substr))
        print()

        cat_mgr.add_criterion(cat_name, substr)
        ledger.add_transaction(cat_name, tx)

        also_found = [tx2 for tx2 in uncategorized[1:]
                      if cat_name == cat_mgr.categorize(tx2.description)]
        if also_found:
            print('I also found these transactions in that category:')
            print()
            for tx2 in also_found:
                ledger.add_transaction(cat_name, tx2)
                print(tx2.pretty_print())
            print()

        uncategorized = [tx2 for tx2 in uncategorized[1:]
                         if tx2 not in also_found]

        time.sleep(2)


def main():
    usage = 'Usage: python3 {} <input-file> <output-file>'.format(sys.argv[0])

    if len(sys.argv) != 3:
        print()
        print('Incorrect number of arguments.')
        print()
        print(usage)
        print()
    else:

        try:
            stmt_path = sys.argv[1]
            output_path = sys.argv[2]

            cat_mgr = CategoryManager()
            stmt_table = Table(stmt_path)

            ledger = Ledger()
            uncategorized = []

            for transaction in stmt_table.rows:
                cat_name = cat_mgr.categorize(transaction.description)
                if cat_name is None:
                    uncategorized += [transaction]
                else:
                    ledger.add_transaction(cat_name, transaction)

            if uncategorized:
                get_categories(uncategorized, cat_mgr, ledger)

            print()
            print()
            print('Saving report...')
            print()
            print()
            with open(output_path, 'w') as f:
                f.write(ledger.pretty_print())

        except KeyboardInterrupt as exc:
            print()
            print()
            print('Exiting...')
            print()
            print()


if __name__ == '__main__':
    main()
