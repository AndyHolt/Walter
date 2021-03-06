"""
Line oriented command interpreter for Walter.

Provides an interactive CLI interface to Walter.
Commands are typed at the command line in order to interact with the finance
database.
"""
# Author: Andy Holt
# Date: Mon 09 Feb 2015 20:58

import cmd
import ledger
from tabulate import tabulate
import datetime

class WalterShell(cmd.Cmd):
    """
    WalterShell class provides a command line interface to walter, using the
    `cmd` library.
    """
    intro = 'Welcome to Walter. Type help or ? to list commands.\n'
    prompt = 'walter: '
    file = None

    # pre and post loop commands
    def preloop(self):
        """
        Set up prior to entering command loop.
        """
        # set up connection to database through ledger object
        # [todo] - select correct database somehow
        self.ledger = ledger.Ledger(db_name='walter_dev')

    def postloop(self):
        """
        Tear down just before exiting command loop.
        """
        # close connection to database through ledger
        self.ledger.close_connection()

    # basic watson commands
    def do_list(self, entity):
        """
        List all types of the entity selected. Default to transactions.

        Arguments:
        - `entity`: the entity type to list. Valid values are 'commands',
            'transactions', 'payees', 'transaction items' and 'categories'
        """
        # set default to transactions
        if entity == '':
            entity = 'transactions'

        try:
            self.validate_entity('list', entity)
        except entityValidationError as err:
            print(err.message)
        else:
            if entity == 'transactions':
                print(tabulate(self.ledger.get_transactions(),
                               headers="keys", tablefmt="psql"))
            elif entity == 'payees':
                print(tabulate(self.ledger.get_payees(),
                               headers="keys", tablefmt="psql"))
            elif entity == 'transaction items':
                print(tabulate(self.ledger.get_items(),
                               headers="keys", tablefmt="psql"))
            elif entity == 'categories':
                print(tabulate(self.ledger.get_categories(),
                               headers="keys", tablefmt="psql"))
            else:
                print('Command not recognised')

    def do_add(self, entity):
        """
        Add a record of the given type to the database. Default to transaction.

        Arguments:
        - `entity`: the entity type to be added. Valid values are:
            'transaction', 'payee', 'transaction_item' and 'category'
        """
        # set default behaviour to add a transaction
        if entity == '':
            entity = 'transaction'

        try:
            self.validate_entity('add', entity)
        except entityValidationError as err:
            print(err.message)
        else:
            self.add_entity(entity)

    def do_edit(self, entity):
        """
        Edit a record in the databas of the given type.

        Arguments:
        - `entity`: the entity type to be edited. Valid values are
            'transaction', 'payee', 'transaction_item' and 'category'
        """
        print("Edit a {0} in the database.".format(entity))

    def do_delete(self, entity):
        """
        Delete a record from the database.

        Arguments:
        - `entity`: the entity type to be deleted. Valid values are
            'transaction', 'payee', 'transaction_item' and 'category'
        """
        print("Delete a {0} from the database.".format(entity))

    def do_EOF(self, arg):
        """
        Exit walter.
        """
        print('Goodbye!')
        return True

    def do_exit(self, arg):
        """
        Exit walter.
        """
        print('Goodbye!')
        # self.close()
        return True

    def do_quit(self, arg):
        """
        Exit walter.
        """
        print('Goodbye!')
        # self.close()
        return True

    def validate_entity(self, command, entity):
        """
        Validate that `entity` is a valid argument for `command`.

        Arguments:
        - `command`: command type
        - `entity`: recieved entity class
        """
        commands = ['add', 'list', 'edit', 'delete']
        entities = {'add': ['transaction', 'payee', 'transaction item',
                            'category'],
                    'list': ['transactions', 'payees', 'transaction items',
                            'categories'],
                    'edit': ['transaction', 'payee', 'transaction item',
                             'category'],
                    'delete': ['transaction', 'payee', 'transaction item',
                               'category'],}
        if command not in commands:
            # [todo] - raise an exception/error here
            raise entityValidationError('Command {0} is not valid'.format(command))

        if entity not in entities[command]:
            # [todo] - raise an exception/error here
            error_string_l = []
            error_string_l.append((
                "Entity {0} invalid for command {1}.\n"
                "Valid entities are:\n "
            ).format(entity, command))
            [error_string_l.append('\t{0}\n'.format(s)) for s in
             entities[command]]

            error_string = ''.join(error_string_l)
            raise entityValidationError(error_string)

    def add_entity(self, entity, tr_date=None, tr_pid=None, tr_desc=None, tr_amt=None,
                   py_name=None,
                   ti_trid=None, ti_desc=None, ti_amt=None, ti_catid=None,
                   ct_name=None, ct_pid=None):
        """
        Get values for entity to be added and pass to ledger object.
        """
        if entity == 'transaction':
            if tr_date == None:
                d_ip = input("Date (format 21-3-2015): ").split('-')
                tr_date = datetime.date(int(d_ip[2], int(d_ip[1],
                                        int(d_ip[0]))))
            if tr_pid == None:
                tr_pid = int(input("Payee ID: "))
            if tr_desc == None:
                tr_desc = input("Description: ")
            if tr_amt == None:
                tr_amt = float(input("Amount: "))
            self.ledger.add_transaction(tr_date, tr_pid, tr_desc, tr_amt)
        elif entity == 'payee':
            foo = None
        elif entity == 'transaction item':
            foo = None
        elif entity == 'category':
            foo = None
        else:
            raise entityValidationError('add_entity recieved invalid entity.')


class entityValidationError(Exception):
    """
    Command has been given an argument which is invalid.
    """
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    WalterShell().cmdloop()
