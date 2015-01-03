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
        self.dbcon.close()


    def get_transactions(self):
        """
        Return a list of dicts of all transactions.
        """
        # open a cursor object
        cur = self.dbcon.cursor()

        # get data from database
        cur.execute("SELECT * FROM transactions")
        data = cur.fetchall()

        # convert into a dict of values.
        trans = []
        [trans.append({'transaction_id': tr[0],
                       'date': tr[1],
                       'payee_id': tr[2],
                       'description': tr[3],
                       'amount': tr[4]})
         for tr in data]

        cur.close()

        return trans
