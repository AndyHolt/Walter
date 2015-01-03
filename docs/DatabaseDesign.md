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

| Column name    | Data type                | Description                                                      |
|----------------|--------------------------|------------------------------------------------------------------|
| transaction_id | SERIAL                   | Unique ID for transaction (also serves as primary key)           |
| date           | DATE                     | Date of transaction                                              |
| payee_id       | BIGINT UNSIGNED NOT NULL | Unique ID of PAYEE (or payer) - relates to PAYEES table          |
| description    | VARCHAR(100)             | Variable length string describing the transaction                |
| amount         | DECIMAL(10,2)            | Value of transaction - negative for expense, positive for income |

The SERIAL data type is an alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT
UNIQUE and is therefore very useful for PRIMARY KEYS.

The DECIMAL(10,2) data type is an "exact" floating point number with 10 digits,
two decimal places (meaning up to 8 digits before the decimal place).

## Transaction Item Table

The transaction item table has 2 purposes:
1. For transactions with multiple purchases or items, these can be broken down
   into the sub-transactions (e.g. different items while shopping).
2. Transactions may be categorised using the breakdown table. The breakdown
   table relates transactions to categories, through sub-purchases if these
   exist. This allows different items in a single purchase to receive different
   categories.
The table has this form:

| transaction_item_id | transaction_id | description                         | amount | category_id |
|---------------------|----------------|-------------------------------------|--------|-------------|
|                   1 |              1 | Train ticket: Aberdeen to Cambridge |  46.85 |           3 |
|                   2 |              2 | Apples                              |   3.00 |           4 |
|                   3 |              2 | Milk                                |   1.00 |           5 |
|                   4 |              2 | Bread                               |   1.42 |           5 |

The columns are:

| Column name         | Data type                | Description                                               |
|---------------------|--------------------------|-----------------------------------------------------------|
| transaction_item_id | SERIAL                   | Unique ID for transaction (PRIMARY KEY)                   |
| transaction_id      | BIGINT UNSIGNED NOT NULL | Links to transaction in TRANSACTIONS table                |
| description         | VARCHAR(100)             | Variable length string describing item                    |
| amount              | DECIMAL(10,2)            | Value of item - negative for expense, positive for income |
| category id         | BIGINT UNSIGNED NOT NULL | Unique ID of category - relates to CATEGORIES table       |

## Payees table

The payees table contains information about payees, which is referenced by their
unique IDs in the transactions table.

| payee_id | payee_name    |
|----------|---------------|
|        1 | National Rail |
|        2 | Sainsbury's   |

The columns are:

| Column name | Data type    | Description                       |
|-------------|--------------|-----------------------------------|
| payee_id    | SERIAL       | Unique ID for Payee (PRIMARY KEY) |
| payee_name  | VARCHAR(100) | Name of payee                     |

## Categories table

The categories table contains categories/tags for the transactions. These allow
spending to be tracked by different budget areas. Categories are grouped
hierarchically through parent categories.

| category_id | parent_id | category_name |
|-------------|-----------|---------------|
|           1 |      NULL | travel        |
|           2 |      NULL | food          |
|           3 |         1 | train         |
|           4 |         2 | fruit         |
|           5 |         2 | staple        |

The columns are:

| Column name   | Data type       | Description                          |
|---------------|-----------------|--------------------------------------|
| category_id   | SERIAL          | Unique ID for category (PRIMARY KEY) |
| parent_id     | BIGINT UNSIGNED | ID of parent category                |
| category_name | VARCHAR(100)    | Category name                        |
