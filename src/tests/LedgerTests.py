"""
Unit tests for Ledger class.
"""
# Author: Andy Holt
# Date: Sat 03 Jan 2015 19:07

import unittest
import datetime
from decimal import *
from Ledger import Ledger

class LedgerTests(unittest.TestCase):

    def setUp(self):
        """
        Initialisation for tests.
        """
        self.ledger = Ledger(db_name='walter_dev')

    def tearDown(self):
        """
        Tidy up after running test.
        """
        self.ledger.close_connection()

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
