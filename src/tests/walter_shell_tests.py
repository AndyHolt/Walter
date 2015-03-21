"""
Unit tests for WalterShell class.

"""
# Author: Andy Holt
# Date: Tue 10 Feb 2015 22:40

# [todo] - don't use ledger at all in this test module.
#   need to separate unit tests of ledger and shell, can test their combined use
#   in integration tests, but don't do it in unit tests.

import subprocess
import unittest
from mock import MagicMock
import walter_shell
import ledger
from decimal import Decimal
import datetime

class WalterShellTests(unittest.TestCase):
    """
    Unit test suite for WalterShell class.
    """
    @classmethod
    def setUpClass(self):
        """
        Initialisation before running test class (run only once).
        """
        # [todo] - need some method of providing a consistent database
        # experience. Perhaps mocking is the way to go.

    def setUp(self):
        """
        Initialisation for tests.
        """
        self.ws = walter_shell.WalterShell()
        # [review] - probably need to run self.ws.preloop() here
        self.ws.preloop()

    def tearDown(self):
        """
        Tidy up after running test.
        """
        # [review] - probably run self.ws.postloop() here
        self.ws.postloop()
        self.ws.onecmd('exit')

    def test_list_default(self):
        """
        Walter Shell `list` command test

        Ensure transactions are correctly fetched and listed for `list`
        command.
        """
        # set up mock method on ledger to test that it is called correctly
        get_trns_return = [{'date': datetime.date(2015, 1, 2),
                            'amount': Decimal('46.85'),
                            'description': 'Train ticket',
                            'transaction_id': 1,
                            'payee_id': 1},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'Shopping',
                            'transaction_id': 2,
                            'payee_id': 2}]
        self.ws.ledger.get_transactions = MagicMock(return_value =
                                                    get_trns_return)

        self.ws.onecmd('list')
        self.ws.ledger.get_transactions.assert_called_with()

    def test_list_transactions(self):
        """
        Walter Shell `list transactions` command test.

        Ensure transactions are correctly fetched and displayed on `list
        transactions` command.
        """
        get_trns_return = [{'date': datetime.date(2015, 1, 2),
                            'amount': Decimal('46.85'),
                            'description': 'Train ticket',
                            'transaction_id': 1,
                            'payee_id': 1},
                           {'date': datetime.date(2015, 1, 3),
                            'amount': Decimal('5.42'),
                            'description': 'Shopping',
                            'transaction_id': 2,
                            'payee_id': 2}]
        self.ws.ledger.get_transactions = MagicMock(return_value =
                                                    get_trns_return)

        self.ws.onecmd('list transactions')
        self.ws.ledger.get_transactions.assert_called_with()
        # [todo] - test display of transactions

    def test_list_payees(self):
        """
        Walter Shell `list payees` command test.

        Ensure payees are correctly fetched and displayed on `list payees`
        command.
        """
        get_pye_rtn = [{'payee_id': 1,
                        'payee_name': 'National Rail'},
                       {'payee_id': 2,
                        'payee_name': "Sainsbury's"}]
        self.ws.ledger.get_payees = MagicMock(return_value = get_pye_rtn)

        self.ws.onecmd('list payees')
        self.ws.ledger.get_payees.assert_called_with()
        # [todo] - test display of payees

    def test_list_transaction_items(self):
        """
        Walter Shell `list transaction items` command test.

        Ensures transaction items are correctly fetched and displayed on `list
        transaction items` command.
        """
        get_items_rtn = [{'transaction_item_id': 1,
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
        self.ws.ledger.get_items = MagicMock(return_value = get_items_rtn)

        self.ws.onecmd('list transaction items')
        self.ws.ledger.get_items.assert_called_with()
        # [todo] - test display of transaction items

    def test_list_categories(self):
        """
        Walter Shell `list categories` command test.

        Ensures categories are correctly fetched and displayed on `list
        transaction items` command.
        """
        get_cat_rtn = [{'category_id': 1,
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
        self.ws.ledger.get_categories = MagicMock(return_value = get_cat_rtn)

        self.ws.onecmd('list categories')
        self.ws.ledger.get_categories.assert_called_with()

    # def test_list_commands(self):
        # [todo] - impelement test_list_commands

    # [todo] - implement test_add_transaction

    # [todo] - implement test_add_payee

    # [todo] - implement test_add_transaction_item

    # [todo] - implement test_add_category

    # [todo] - implement test_edit_transaction

    # [todo] - implement test_edit_payee

    # [todo] - implement test_edit_transaction_item

    # [todo] - implement test_edit_category

    # [todo] - implement test_delete_transaction

    # [todo] - implement test_delete_payee

    # [todo] - implement test_delete_transaction_item

    # [todo] - implement test_delete_category
