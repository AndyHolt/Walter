"""
Interface to data base.

"""
# Author: Andy Holt
# Date: Sat 03 Jan 2015 17:59

import pymysql as pysql

class Ledger:
    """
    Interface to database.

    Provides methods for accessing and modifying database entries.
    """
    def __init__(self, db_name):
        """
        Set up connection to database.
        """
        if db_name == "":
            db_name = "walter"

        self.dbcon =  pysql.connect(user='walter', db=db_name)

    def close_connection(self):
        """
        Close connection to database. Must be called when finished.
        """
        self.dbcon.commit()
        self.dbcon.close()

    def get_cursor(self):
        """
        Return a cursor object for use by any method interacting with database.
        """
        self.cur = self.dbcon.cursor()
        return self.cur

    def close_cursor(self, cursor=None):
        """
        Close a cursor.

        If cursor is passed, close that cursor. Otherwise, close the default
        object cursor, self.cur

        Arguments:
        - `cursor`: Optional cursor to be closed
        """
        if cursor != None:
            cursor.close()
        else:
            self.cur.close()

        self.dbcon.commit()

    def reset_auto_increment(self, table_name):
        """
        Reset the AUTO_INCREMENT counter for given table.

        Arguments:
        - `table_name`: table to reset counter of
        """
        cur = self.get_cursor()

        # lookup for primary key column name
        keys = {'categories': 'category_id',
                'payees': 'payee_id',
                'transaction_items': 'transaction_item_id',
                'transactions': 'transaction_id'}

        # get current max value
        get_max_statement = "SELECT MAX({0}) FROM {1}".format(keys[table_name],
                                                              table_name)
        cur.execute(get_max_statement)
        max_key_value = cur.fetchall()[0][0]

        # reset AUTO_INCREMENT counter
        reset = "ALTER TABLE {0} AUTO_INCREMENT = {1}".format(table_name,
                                                              max_key_value+1)
        cur.execute(reset)

        self.close_cursor()

    def add_payee(self, payee_name):
        """
        Add a payee to the database.

        Arguments:
        - `payee_name`: Name of the payee
        """
        # [todo] - add check that payee_name is unique

        # open a cursor
        cur = self.get_cursor()

        self.reset_auto_increment('payees')

        # add payee with given name
        add_payee_statement = "INSERT INTO payees " + \
                              "VALUES ('0', '{0}')".format(payee_name)

        cur.execute(add_payee_statement)

        # close cursor
        self.close_cursor()

    def edit_payee(self, payee_id, new_payee_name):
        """
        Give a payee a new name.

        Arguments:
        - `payee_id`: payee to be modified
        - `new_payee_name`: new name for the payee
        """
        # [todo] - add check that new_payee_name is unique

        # open a cursor
        cur = self.get_cursor()

        edit_payee_statement = "UPDATE payees " + \
                               "SET payee_name='{0}' ".format(new_payee_name) + \
                               "WHERE payee_id={0}".format(payee_id)

        cur.execute(edit_payee_statement)

        # close the cursor
        self.close_cursor()

    def delete_payee(self, payee_id):
        """
        Remove a payee from the database

        Arguments:
        - `payee_id`: payee to be deleted
        """
        # [todo] - handle deletion failure
        #   probably best done by catching exception raised if the payee has
        #   children in transactions table

        # open a cursor
        cur = self.get_cursor()

        delete_payee_statement = "DELETE FROM payees " + \
                                 "WHERE payee_id={0}".format(payee_id)
        cur.execute(delete_payee_statement)

        # close the cursor
        self.close_cursor()


    def get_payees(self):
        """
        Return a list of dicts of all payees.
        """
        # open a cursor object
        cur = self.get_cursor()

        # get payees from database
        cur.execute("SELECT * FROM payees")
        payees_data = cur.fetchall()

        # convert into a list of payee dictionaries
        payees_list = []
        [payees_list.append({'payee_id': payee[0],
                             'payee_name': payee[1]})
         for payee in payees_data]

        # close the cursor
        self.close_cursor()

        return payees_list

    def get_transactions(self):
        """
        Return a list of dicts of all transactions.
        """
        # open a cursor object
        cur = self.get_cursor()

        # get transactions from database
        cur.execute("SELECT * FROM transactions")
        transactions_data = cur.fetchall()

        # convert into a dict of values.
        transactions_list = []
        [transactions_list.append({'transaction_id': transaction[0],
                                   'date': transaction[1],
                                   'payee_id': transaction[2],
                                   'description': transaction[3],
                                   'amount': transaction[4]})
         for transaction in transactions_data]

        # close the cursor
        self.close_cursor()

        return transactions_list

    def add_transaction(self, date, payee_id, description, amount):
        """
        Add a transaction to the database with the specified values.

        Arguments:
        - `date`: A datetime.date object consisting of the date.
        - `payee_id`: The payee_id of the payee.
        - `description`: String describing the transaction.
        - `amount`: Amount of transaction
        """
        # [todo] - implement error handling and parameter checking pre-execution

        # open a cursor
        cur = self.get_cursor()

        self.reset_auto_increment('transactions')

        # add transaction with required values
        stmt = "INSERT INTO transactions " + \
               "VALUES ('0', " + \
               "'{0}-{1}-{2}', ".format(date.year, date.month, date.day) + \
               "'{0}', '{1}', ".format(payee_id, description) + \
               "'{0}')".format(amount)

        cur.execute(stmt)

        # close the cursor
        self.close_cursor()

    def edit_transaction(self, trans_id, date, payee_id, description, amount):
        """
        Edit transaction trans_id to take on new values.

        Arguments:
        - `trans_id`: transasction to be modified
        - `date`: new date
        - `payee_id`: new payee id
        - `description`: new description
        - `amount`: new amount
        """
        # [todo] - all parameters except trans_id optional, fill others with
        # current values

        # [todo] - validate transaction_id
        # [todo] - validate new values

        # open a cursor
        cur = self.get_cursor()

        edit_trans_statement = "UPDATE transactions " + \
                               "SET date='{0}-{1}-{2}', ".format(date.year,
                                                                 date.month,
                                                                 date.day) + \
                               "payee_id='{0}', ".format(payee_id) + \
                               "description='{0}', ".format(description) + \
                               "amount='{0}' ".format(amount) + \
                               "WHERE transaction_id={0}".format(trans_id)

        cur.execute(edit_trans_statement)

        # close the cursor
        self.close_cursor()

    def delete_transaction(self, trans_id):
        """
        Delete transaction with id trans_id

        Arguments:
        - `trans_id`: id of transaction to be deleted.
        """
        # [todo] - ensure no transaction_items depend on transaction to be
        # deleted

        # open a cursor
        cur = self.get_cursor()

        delete_trans_statement = "DELETE FROM transactions " + \
                                 "WHERE transaction_id={0}".format(trans_id)

        cur.execute(delete_trans_statement)

        # close the cursor
        self.close_cursor()

    def get_items(self):
        """
        Return a list of dicts of all transaction items.
        """
        # open a cursor object
        cur = self.get_cursor()

        # get payees from database
        cur.execute("SELECT * FROM transaction_items")
        items_data = cur.fetchall()

        # convert into a list of payee dictionaries
        items_list = []
        [items_list.append({'transaction_item_id': item[0],
                            'transaction_id': item[1],
                            'description': item[2],
                            'amount': item[3],
                            'category_id': item[4]})
         for item in items_data]

        # close the cursor
        self.close_cursor()

        return items_list

    def add_item(self, transaction_id, description, amount, category_id):
        """
        Add a transaction item to the database with the specified values.

        Arguments:
        - `transaction_id`: transaction to be associated to
        - `description`: String describing the transaction.
        - `amount`: Amount of transaction
        - `category_id` category that item belongs to
        """
        # [todo] - implement error handling and parameter checking pre-execution

        # open a cursor
        cur = self.get_cursor()

        self.reset_auto_increment('transaction_items')

        # add transaction with required values
        stmt = "INSERT INTO transaction_items " + \
               "VALUES ('0', " + \
               "'{0}', '{1}', ".format(transaction_id, description) + \
               "'{0}', '{1}')".format(amount, category_id)

        cur.execute(stmt)

        # close the cursor
        self.close_cursor()

    def edit_item(self, item_id, transaction_id, description, amount,
                  category_id):
        """
        Edit transaction item item_id to take on new values.

        Arguments:
        - `item_id`: item to be modified
        - `transaction_id`: new transaction to be associated with
        - `description`: new description of item
        - `amount`: new amount of item
        - `category_id`: new category assignment
        """
        # [todo] - all parameters except item_id optional, fill others with
        # current values

        # [todo] - validate item_id
        # [todo] - validate new values

        # open a cursor
        cur = self.get_cursor()

        stmt = "UPDATE transaction_items " + \
               "SET transaction_id='{0}', ".format(transaction_id) + \
               "description='{0}', ".format(description) + \
               "amount='{0}', ".format(amount) + \
               "category_id='{0}' ".format(category_id) + \
               "WHERE transaction_item_id={0}".format(item_id)

        cur.execute(stmt)

        # close the cursor
        self.close_cursor()

    def delete_item(self, item_id):
        """
        Delete transaction item with id item_id

        Arguments:
        - `item_id`: id of transaction item to be deleted.
        """
        # open a cursor
        cur = self.get_cursor()

        delete_item_statement = "DELETE FROM transaction_items " + \
                                "WHERE transaction_item_id={0}".format(item_id)

        cur.execute(delete_item_statement)

        # close the cursor
        self.close_cursor()

    def get_categories(self):
        """
        Return a list of dicts of all categories.
        """
        # open a cursor object
        cur = self.get_cursor()

        # get payees from database
        cur.execute("SELECT * FROM categories")
        cats_data = cur.fetchall()

        # convert into a list of payee dictionaries
        cats_list = []
        [cats_list.append({'category_id': cat[0],
                           'parent_id': cat[1],
                           'category_name': cat[2]})
         for cat in cats_data]

        # close the cursor
        self.close_cursor()

        return cats_list

    def add_category(self, category_name, parent_id):
        """
        Add a category to the database with the specified name and parent.

        Arguments:
        - `category_name`: category name
        - `parent_id`: id of parent category to which this is a direct child
        """
        # [todo] - implement error handling and parameter checking pre-execution

        # open a cursor
        cur = self.get_cursor()

        self.reset_auto_increment('categories')

        # add transaction with required values
        stmt = "INSERT INTO categories " + \
               "VALUES ('0', " + \
               "'{0}', '{1}')".format(parent_id, category_name)

        cur.execute(stmt)

        # close the cursor
        self.close_cursor()

    def edit_category(self, category_id, category_name, parent_id):
        """
        Edit category category_id to take on new values.

        Arguments:
        - `category_id`: category to be edited
        - `category_name`: new name of category
        - `parent_id`: new parent for category
        """
        # [todo] - all parameters except category_id optional, fill others with
        # current values

        # [todo] - validate category_id
        # [todo] - validate new values

        # open a cursor
        cur = self.get_cursor()

        stmt = "UPDATE categories " + \
               "SET parent_id='{0}', ".format(parent_id) + \
               "category_name='{0}' ".format(category_name) + \
               "WHERE category_id={0}".format(category_id)

        cur.execute(stmt)

        # close the cursor
        self.close_cursor()

    def delete_category(self, category_id):
        """
        Delete category with id category_id

        Arguments:
        - `category_id`: id of category to be deleted.
        """
        # [todo] - add error handling

        # open a cursor
        cur = self.get_cursor()

        delete_cat_statement = "DELETE FROM categories " + \
                               "WHERE category_id={0}".format(category_id)

        cur.execute(delete_cat_statement)

        # close the cursor
        self.close_cursor()
