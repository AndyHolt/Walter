"""
Line oriented command interpreter for Walter.

Provides an interactive CLI interface to Walter.
Commands are typed at the command line in order to interact with the finance
database.
"""
# Author: Andy Holt
# Date: Mon 09 Feb 2015 20:58

import cmd

class WalterShell(cmd.Cmd):
    """
    WalterShell class provides a command line interface to walter, using the
    `cmd` library.
    """
    intro = 'Welcome to Walter. Type help or ? to list commands.\n'
    prompt = 'walter: '
    file = None

    # basic watson commands
    def do_list(self, entity):
        """
        List all types of the entity selected. Default to transactions.

        Arguments:
        - `entity`: the entity type to list. Valid values are 'commands',
            'transactions', 'payees', 'transaction_items' and 'categories'
        """
        try:
            self.validate_entity('list', entity)
        except entityValidationError as err:
            print(err.message)
        else:
            print("Produce list of all {0}.".format(entity))

    def do_add(self, entity):
        """
        Add a record of the given type to the database. Default to transaction.

        Arguments:
        - `entity`: the entity type to be added. Valid values are:
            'transaction', 'payee', 'transaction_item' and 'category'
        """
        print("Add a {0} to the database.".format(entity))

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
        entities = {'add': ['transaction', 'payee', 'transaction_item',
                            'category'],
                    'list': ['transactions', 'payees', 'transaction_items',
                            'categories'],
                    'edit': ['transaction', 'payee', 'transaction_item',
                             'category'],
                    'delete': ['transaction', 'payee', 'transaction_item',
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

class entityValidationError(Exception):
    """
    Command has been given an argument which is invalid.
    """
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    WalterShell().cmdloop()
