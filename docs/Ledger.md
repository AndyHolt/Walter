# Ledger

The Ledger class provides an interface to the database for other classes to
interact with. Very simple class, no processing occurs here - that will be done
by higher classes.

## Methods

These will probably be extended as new features are required.

### Add Payee

add_payee(payee_name)

Add a payee to the payees table.

### Edit Payee

edit_payee(id, new_name)

Rename payee id with new_name.

### Delete Payee

delete_payee(id)

Delete payee id.

### Get Payees

[payee] = get_payees()

Return an array of dictionaries of all payees.

### Add Transaction

add_transaction(date, payee_id, description, amount)

Add a transaction to the transactions table.

### Edit Transaction

edit_transaction(id, date, payee_id, description, amount)

Modify transaction id values for other fields.

### Delete Transaction

delete_transaction(id)

Delete transaction id.

### Get Transactions

[transaction] = get_transactions()

Return an array of dictionaries of all transactions.

### Add Item

add_item(transaction_id, description, amount, category_id)

Add transaction item to transaction_items table.

### Edit Item

edit_item(id, transaction_id, description, amount, category_id)

Modify item id values for other fields.

### Delete Item

delete_item(id)

Delete item id.

### Get Items

[item] = get_items()

Return an array of dictionaries of all items.

### Add Category

add_category(category_name, parent_id)

Add a category to table.

### Edit Category

edit_category(id, category_name, parent_id)

Modify category id values for other fields.

### Delete Category

delete_category(id)

Delete category id.

### Get Categories

[category] = get_categories()

Return an array of dictionaries of all categories.
