"""
Unit tests for Ledger class.
"""
# Author: Andy Holt
# Date: Sat 03 Jan 2015 19:07

import unittest
import datetime
from decimal import *
import pymysql as pysql
from ledger import Ledger

class LedgerTests(unittest.TestCase):

    def setUp(self):
        """
        Initialisation for tests.
        """
        dbcon = pysql.connect(user='walter', db='walter_dev')
        cur = dbcon.cursor()

        # set up database to known state
        statement = "INSERT INTO payees " + \
                      "VALUES (1, 'National Rail'), " + \
                             "(2, 'Sainsbury''s')"
        cur.execute(statement)

        statement = "INSERT INTO transactions " + \
                      "VALUES (1, '2015-01-02', 1, 'Train ticket', 46.85), " + \
                             "(2, '2015-01-03', 2, 'Shopping', 5.42)"
        cur.execute(statement)

        statement = "INSERT INTO categories " + \
                      "VALUES (1, NULL, 'travel'), " + \
                             "(2, NULL, 'food'), " + \
                             "(3, 1, 'train'), " + \
                             "(4, 2, 'fruit'), " + \
                             "(5, 2, 'staple')"
        cur.execute(statement)

        statement = "INSERT INTO transaction_items " + \
                        "VALUES (1, 1, 'Train ticket: Aberdeen to Cambridge', 46.85, 3), " + \
                               "(2, 2, 'Apples', 3.00, 4), " + \
                               "(3, 2, 'Milk', 1.00, 5), " + \
                               "(4, 2, 'Bread', 1.42, 5)"
        cur.execute(statement)

        cur.close()
        dbcon.commit()
        dbcon.close()

        # create Ledger object
        self.ledger = Ledger(db_name='walter_dev')

    def tearDown(self):
        """
        Tidy up after running test.
        """
        # close connection of Ledger object
        self.ledger.close_connection()

        # remove entries from database
        dbcon = pysql.connect(user='walter', db='walter_dev')
        cur = dbcon.cursor()

        statement = "DELETE FROM transaction_items " + \
                    "WHERE transaction_item_id != 0"
        cur.execute(statement)
        statement = "DELETE FROM categories " + \
                    "WHERE parent_id != 'NULL'"
        cur.execute(statement)
        statement = "DELETE FROM categories " + \
                    "WHERE category_id != 0"
        cur.execute(statement)
        statement = "DELETE FROM transactions " + \
                    "WHERE transaction_id != 0"
        cur.execute(statement)
        statement = "DELETE FROM payees " + \
                    "WHERE payee_id != 0"
        cur.execute(statement)

        cur.close()
        dbcon.commit()
        dbcon.close()

    def test_get_transasctions(self):
        """
        Ensure transactions are correctly recieved from database.
        """
        expected_result = [{'date': datetime.date(2015, 1, 2),
                            'amount': Decimal('46.85'),
                            'description': 'Train ticket',
                            'transaction_id': 1,
                            'payee_id': 1},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'Shopping',
                            'transaction_id': 2,
                            'payee_id': 2}]
        actual_result = self.ledger.get_transactions()

        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main
