# Command Line Interface

Command line interface to Walter - how the user interacts with the programme. 2
modes are given:
- Interactive mode: user enters an interactive session with Walter.
- Batch mode: provides traditional unixy functionality - get data from stdin,
  process in response to options and switches, return to stdout.

## Interactive mode

When in interactive mode, one of the operations may be selected by typing its
name at the command prompt. The following commands are available:
- **help**
  Displays a help message explaining what can be done
- **list** [commands | transactions | payees | transaction_items | categories]
  Lists all types of the entity selected. Default to transactions.
  - **commands**: print a list of commands to console
  - **transactions**: show a nicely formatted table of transactions (possibly use
    `less` to display when longer than a certain length?)
  - **payees**: print a list of payees to console
  - **transaction_items**: print a nicely formatted table of transaction items
    (probably listed below each transaction?)
  - **categories**: (possible alias - tags) print all categories (probably
    sorted by parent category, with children shown below each parent)
- **add** [transaction | payee | transaction_item | category]
  Add to the database a record of the given type.
  - **transaction**: add a transaction to database - this will go through a
    series of prompts for the different values (date, payee (show list of
    payees?), amount etc). Also ask for items (using transaction_item interface code)
  - **payee**: add a payee to the database
  - **transaction_item**: add an item to the given transaction, provide a series
    of prompts for the values
  - **category**: add a new category, prompts for category name and parent
    (show list of parent candidates?)
- **edit** [transaction | payee | transaction_item | category]
  Edit a particular entity: show list of possible things of selected type with
  numerical values to select which, then a series of prompts to select which to use.
  - **transaction**: Also check whether items need editing(using
    transaction_item interface code)
  - **payee**:
  - **transaction_item**:
  - **category**:
- **delete** [transaction | payee | transaction_item | category]
  Delete a particular entity: show list of possible things of selected type with
  numerical values to select which, then a series of prompts to select which to
  delete.
  - **transaction**: Also check whether items need editing(using
    transaction_item interface code)
  - **payee**:
  - **transaction_item**:
  - **category**:

### Implementation

Uses `cmd` class to produce a line-oriented command interpreter.

## Batch mode

Uses `Cement` framework for command line applications.
