-- File name: Walter/src/DatabaseEmpty.sql
-- Remove all data from database, leaving just empty tables.
-- Author: adh
-- Date: Sat 03 Jan 2015 15:55

-- [todo] - delete data from test database
USE walter_dev;

DELETE FROM transaction_items WHERE transaction_item_id != 0;
DELETE FROM categories WHERE parent_id != 'NULL';
DELETE FROM categories WHERE category_id != 0;
DELETE FROM transactions WHERE transaction_id != 0;
DELETE FROM payees WHERE payee_id != 0;

SELECT * FROM transactions;
SELECT * FROM transaction_items;
SELECT * FROM payees;
SELECT * FROM categories;
