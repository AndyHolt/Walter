# Database design

Database records financial transactions with the following data:
- Date
- Payee
- Category
- Description
- Amount

It would be useful to track individual items within a transaction, for example
if shopping, as different purchases in a single transaction may have very
different categories. A separate purchase table should therefore be used.

## Transactions Table

The transactions table is the core of the database, and has a form as following:

| transaction_id |       date | payee_id | description  | amount |
|----------------|------------|----------|--------------|--------|
|              1 | 2015-01-02 |        1 | Train ticket |  46.85 |
|              2 | 2015-01-03 |        2 | Shopping     |   5.42 |

The columns are:

| Column name    | Data type      | Description                                                      |
|----------------|----------------|------------------------------------------------------------------|
| transaction_id | INT            | Unique ID for transaction (also serves as primary key)           |
| date           | DATE           | Date of transaction                                              |
| payee_id       | INT            | Unique ID of PAYEE (or payer) - relates to PAYEES table          |
| description    | STRING         | Variable length string describing the transaction                |
| amount         | FLOAT with 2dp | Value of transaction - negative for expense, positive for income |


## Transaction Item Table

The transaction item table has 2 purposes:
1. For transactions with multiple purchases or items, these can be broken down
   into the sub-transactions (e.g. different items while shopping).
2. Transactions may be categorised using the breakdown table. The breakdown
   table relates transactions to categories, through sub-purchases if these
   exist. This allows different items in a single purchase to receive different
   categories.
The table has this form:

<!-- [todo] - change categories to ints and use categories table -->
| transaction_item_id | transaction_id | description                         | amount | category_id |
|---------------------|----------------|-------------------------------------|--------|-------------|
|                   1 |              1 | Train ticket: Aberdeen to Cambridge |  46.85 |           3 |
|                   2 |              2 | Apples                              |   3.00 |           4 |
|                   3 |              2 | Milk                                |   1.00 |           5 |
|                   4 |              2 | Bread                               |   1.42 |           5 |

The columns are:

| Column name         | Data type      | Description                                               |
|---------------------|----------------|-----------------------------------------------------------|
| transaction_item_id | INT            | Unique ID for transaction (PRIMARY KEY)                   |
| transaction_id      | INT            | Links to transaction in TRANSACTIONS table                |
| description         | STRING         | Variable length string describing item                    |
| amount              | FLOAT with 2dp | Value of item - negative for expense, positive for income |
| category id         | INT            | Unique ID of category - relates to CATEGORIES table       |

## Payees table

The payees table contains information about payees, which is referenced by their
unique IDs in the transactions table.

| payee_id | payee_name    |
|----------|---------------|
|        1 | National Rail |
|        2 | Sainsbury's   |

The columns are:

| Column name | Data type | Description                       |
|-------------|-----------|-----------------------------------|
| payee_id    | INT       | Unique ID for Payee (PRIMARY KEY) |
| payee_name  | STRING    | Name of payee                     |

## Categories table

The categories table contains categories/tags for the transactions. These allow
spending to be tracked by different budget areas. Categories are grouped
hierarchically through parent categories.

| category_id | category | parent_id |
|-------------|----------|-----------|
|           1 | travel   |      NULL |
|           2 | food     |      NULL |
|           3 | train    |         1 |
|           4 | fruit    |         2 |
|           5 | staple   |         2 |

The columns are:

| Column name | Data type | Description                          |
|-------------|-----------|--------------------------------------|
| category_id | INT       | Unique ID for category (PRIMARY KEY) |
| category    | STRING    | Category name                        |
| parent_id   | INT       | ID of parent category                |
