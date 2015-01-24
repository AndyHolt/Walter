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

    def test_get_payees(self):
        """
        Ensure payees are correctly recieved from database.
        """
        expected_result = [{'payee_id': 1,
                            'payee_name': 'National Rail'},
                           {'payee_id': 2,
                            'payee_name': "Sainsbury's"}]
        actual_result = self.ledger.get_payees()

        self.assertEqual(actual_result, expected_result)

    def test_add_payee(self):
        """
        Ensure a payee is correctly added to the database.
        """
        self.ledger.add_payee('Waitrose')

        expected_result = [{'payee_id': 1,
                            'payee_name': 'National Rail'},
                           {'payee_id': 2,
                            'payee_name': "Sainsbury's"},
                           {'payee_id': 3,
                            'payee_name': 'Waitrose'}]
        actual_result = self.ledger.get_payees()

        self.assertEqual(actual_result, expected_result)

    def test_edit_payee(self):
        """
        Test modification of a payee using edit_payee method.
        """
        self.ledger.edit_payee(2, 'Tesco')

        expected_result = [{'payee_id': 1,
                            'payee_name': 'National Rail'},
                           {'payee_id': 2,
                            'payee_name': 'Tesco'}]
        actual_result = self.ledger.get_payees()

        self.assertEqual(actual_result, expected_result)

    def test_delete_payee(self):
        """
        Test deletion of a payee using delete_payee method.
        """
        # first, add a payee with no associated transactions
        self.ledger.add_payee('Waitrose')
        expected_result = [{'payee_id': 1,
                            'payee_name': 'National Rail'},
                           {'payee_id': 2,
                            'payee_name': "Sainsbury's"},
                           {'payee_id': 3,
                            'payee_name': 'Waitrose'}]
        actual_result = self.ledger.get_payees()
        self.assertEqual(actual_result, expected_result)

        # then delete the new payee to make sure it's gone
        self.ledger.delete_payee(3)

        expected_result = [{'payee_id': 1,
                            'payee_name': 'National Rail'},
                           {'payee_id': 2,
                            'payee_name': "Sainsbury's"}]
        actual_result = self.ledger.get_payees()

        self.assertEqual(actual_result, expected_result)

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

    def test_add_transaction(self):
        """
        Ensure that transactions are correctly added to database
        """
        self.ledger.add_transaction(datetime.date(2015, 1, 3),
                                    2,
                                    'More shopping',
                                    5.42)

        expected_result = [{'date': datetime.date(2015, 1, 2),
                            'amount': Decimal('46.85'),
                            'description': 'Train ticket',
                            'transaction_id': 1,
                            'payee_id': 1},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'Shopping',
                            'transaction_id': 2,
                            'payee_id': 2},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'More shopping',
                            'transaction_id': 3,
                            'payee_id': 2}]
        actual_result = self.ledger.get_transactions()

        self.assertEqual(actual_result, expected_result)

    def test_edit_transaction(self):
        """
        Test modification of a transaction using edit_transaction_method.
        """
        self.ledger.edit_transaction(2,
                                     datetime.date(2015,1,5),
                                     1,
                                     'Another train ticket',
                                     42.00)

        expected_result = [{'date': datetime.date(2015, 1, 2),
                            'amount': Decimal('46.85'),
                            'description': 'Train ticket',
                            'transaction_id': 1,
                            'payee_id': 1},
                           {'date': datetime.date(2015, 1, 5),
                            'amount': Decimal('42.00'),
                            'description': 'Another train ticket',
                            'transaction_id': 2,
                            'payee_id': 1}]
        actual_result = self.ledger.get_transactions()

        self.assertEqual(actual_result, expected_result)

    def test_delete_transaction(self):
        """
        Test deletion of a transaction using delete_transaction method.
        """
        # first, create a transaction with no dependents
        self.ledger.add_transaction(datetime.date(2015, 1, 3),
                                    2,
                                    'More shopping',
                                    5.42)
        expected_result = [{'date': datetime.date(2015, 1, 2),
                            'amount': Decimal('46.85'),
                            'description': 'Train ticket',
                            'transaction_id': 1,
                            'payee_id': 1},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'Shopping',
                            'transaction_id': 2,
                            'payee_id': 2},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'More shopping',
                            'transaction_id': 3,
                            'payee_id': 2}]
        actual_result = self.ledger.get_transactions()
        self.assertEqual(actual_result, expected_result)

        # then delete the extra transaction
        self.ledger.delete_transaction(3)

        actual_result = self.ledger.get_transactions()
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
        self.assertEqual(actual_result, expected_result)

    def test_get_items(self):
        """
        Ensure transaction items are correctly recieved from database
        """
        expected_result = [{'transaction_item_id': 1,
                            'transaction_id': 1,
                            'description': 'Train ticket: Aberdeen to Cambridge',
                            'amount': Decimal('46.85'),
                            'category_id': 3},
                           {'transaction_item_id': 2,
                            'transaction_id': 2,
                            'description': 'Apples',
                            'amount': Decimal('3.00'),
                            'category_id': 4},
                           {'transaction_item_id': 3,
                            'transaction_id': 2,
                            'description': 'Milk',
                            'amount': Decimal('1.00'),
                            'category_id': 5},
                           {'transaction_item_id': 4,
                            'transaction_id': 2,
                            'description': 'Bread',
                            'amount': Decimal('1.42'),
                            'category_id': 5}]
        actual_result = self.ledger.get_items()

        self.assertEqual(actual_result, expected_result)

    def test_add_item(self):
        """
        Ensure that transaction items are correctly added to database
        """
        self.ledger.add_item(2, 'Bananas', 0.67, 4)

        expected_result = [{'transaction_item_id': 1,
                            'transaction_id': 1,
                            'description': 'Train ticket: Aberdeen to Cambridge',
                            'amount': Decimal('46.85'),
                            'category_id': 3},
                           {'transaction_item_id': 2,
                            'transaction_id': 2,
                            'description': 'Apples',
                            'amount': Decimal('3.00'),
                            'category_id': 4},
                           {'transaction_item_id': 3,
                            'transaction_id': 2,
                            'description': 'Milk',
                            'amount': Decimal('1.00'),
                            'category_id': 5},
                           {'transaction_item_id': 4,
                            'transaction_id': 2,
                            'description': 'Bread',
                            'amount': Decimal('1.42'),
                            'category_id': 5},
                           {'transaction_item_id': 5,
                            'transaction_id': 2,
                            'description': 'Bananas',
                            'amount': Decimal('0.67'),
                            'category_id': 4}]
        actual_result = self.ledger.get_items()

        self.assertEqual(actual_result, expected_result)

    def test_edit_item(self):
        """
        Test modification of a transaction item using edit_item method.
        """
        self.ledger.edit_item(4, 1, 'More train tickets', 25.34, 3)

        expected_result = [{'transaction_item_id': 1,
                            'transaction_id': 1,
                            'description': 'Train ticket: Aberdeen to Cambridge',
                            'amount': Decimal('46.85'),
                            'category_id': 3},
                           {'transaction_item_id': 2,
                            'transaction_id': 2,
                            'description': 'Apples',
                            'amount': Decimal('3.00'),
                            'category_id': 4},
                           {'transaction_item_id': 3,
                            'transaction_id': 2,
                            'description': 'Milk',
                            'amount': Decimal('1.00'),
                            'category_id': 5},
                           {'transaction_item_id': 4,
                            'transaction_id': 1,
                            'description': 'More train tickets',
                            'amount': Decimal('25.34'),
                            'category_id': 3}]
        actual_result = self.ledger.get_items()

        self.assertEqual(actual_result, expected_result)

    def test_delete_item(self):
        """
        Test deletion of a transaction item using delete_item method.
        """
        self.ledger.delete_item(3)

        expected_result = [{'transaction_item_id': 1,
                            'transaction_id': 1,
                            'description': 'Train ticket: Aberdeen to Cambridge',
                            'amount': Decimal('46.85'),
                            'category_id': 3},
                           {'transaction_item_id': 2,
                            'transaction_id': 2,
                            'description': 'Apples',
                            'amount': Decimal('3.00'),
                            'category_id': 4},
                           {'transaction_item_id': 4,
                            'transaction_id': 2,
                            'description': 'Bread',
                            'amount': Decimal('1.42'),
                            'category_id': 5}]
        actual_result = self.ledger.get_items()
        self.assertEqual(actual_result, expected_result)

    def test_get_categories(self):
        """
        Ensure categories are correctly recieved from database
        """
        expected_result = [{'category_id': 1,
                            'parent_id': None,
                            'category_name': 'travel'},
                           {'category_id': 2,
                            'parent_id': None,
                            'category_name': 'food'},
                           {'category_id': 3,
                            'parent_id': 1,
                            'category_name': 'train'},
                           {'category_id': 4,
                            'parent_id': 2,
                            'category_name': 'fruit'},
                           {'category_id': 5,
                            'parent_id': 2,
                            'category_name': 'staple'}]
        actual_result = self.ledger.get_categories()

        self.assertEqual(actual_result, expected_result)

    def test_add_category(self):
        """
        Ensure that categories are correctly added to database
        """
        self.ledger.add_category('coach', 1)

        expected_result = [{'category_id': 1,
                            'parent_id': None,
                            'category_name': 'travel'},
                           {'category_id': 2,
                            'parent_id': None,
                            'category_name': 'food'},
                           {'category_id': 3,
                            'parent_id': 1,
                            'category_name': 'train'},
                           {'category_id': 4,
                            'parent_id': 2,
                            'category_name': 'fruit'},
                           {'category_id': 5,
                            'parent_id': 2,
                            'category_name': 'staple'},
                           {'category_id': 6,
                            'parent_id': 1,
                            'category_name':'coach'}]
        actual_result = self.ledger.get_categories()

        self.assertEqual(actual_result, expected_result)

    def test_edit_category(self):
        """
        Test modification of a category using edit_category method.
        """
        self.ledger.edit_category(4, 'coach', 1)

        expected_result = [{'category_id': 1,
                            'parent_id': None,
                            'category_name': 'travel'},
                           {'category_id': 2,
                            'parent_id': None,
                            'category_name': 'food'},
                           {'category_id': 3,
                            'parent_id': 1,
                            'category_name': 'train'},
                           {'category_id': 4,
                            'parent_id': 1,
                            'category_name': 'coach'},
                           {'category_id': 5,
                            'parent_id': 2,
                            'category_name': 'staple'}]
        actual_result = self.ledger.get_categories()

        self.assertEqual(actual_result, expected_result)

    def test_delete_category(self):
        """
        Test deletion of a cateory using delete_category method.
        """
        # first, create a category with no dependents
        self.ledger.add_category('coach', 1)
        expected_result = [{'category_id': 1,
                            'parent_id': None,
                            'category_name': 'travel'},
                           {'category_id': 2,
                            'parent_id': None,
                            'category_name': 'food'},
                           {'category_id': 3,
                            'parent_id': 1,
                            'category_name': 'train'},
                           {'category_id': 4,
                            'parent_id': 2,
                            'category_name': 'fruit'},
                           {'category_id': 5,
                            'parent_id': 2,
                            'category_name': 'staple'},
                           {'category_id': 6,
                            'parent_id': 1,
                            'category_name':'coach'}]
        actual_result = self.ledger.get_categories()
        self.assertEqual(actual_result, expected_result)

        # then delete the extra transaction
        self.ledger.delete_category(6)

        expected_result = [{'category_id': 1,
                            'parent_id': None,
                            'category_name': 'travel'},
                           {'category_id': 2,
                            'parent_id': None,
                            'category_name': 'food'},
                           {'category_id': 3,
                            'parent_id': 1,
                            'category_name': 'train'},
                           {'category_id': 4,
                            'parent_id': 2,
                            'category_name': 'fruit'},
                           {'category_id': 5,
                            'parent_id': 2,
                            'category_name': 'staple'}]
        actual_result = self.ledger.get_categories()

        self.assertEqual(actual_result, expected_result)
