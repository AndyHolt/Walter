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
