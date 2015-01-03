-- File name: Walter/src/DatabasePopulate.sql
-- Populate Walter database with some dummy data.
-- Author: adh
-- Date: Sat 03 Jan 2015 15:30

-- [todo] - change to populate test database instead of real one
USE walter;

INSERT INTO payees
       VALUES (1, 'National Rail'),
              (2, 'Sainsbury''s');

INSERT INTO transactions
       VALUES (1, '2015-01-02', 1, 'Train ticket', 46.85),
              (2, '2015-01-03', 2, 'Shopping', 5.42);

INSERT INTO categories
       VALUES (1, NULL, 'travel'),
              (2, NULL, 'food'),
              (3, 1, 'train'),
              (4, 2, 'fruit'),
              (5, 2, 'staple');

INSERT INTO transaction_items
       VALUES (1, 1, 'Train ticket: Aberdeen to Cambridge', 46.85, 3),
              (2, 2, 'Apples', 3.00, 4),
              (3, 2, 'Milk', 1.00, 5),
              (4, 2, 'Bread', 1.42, 5);

SELECT * FROM transactions;
SELECT * FROM transaction_items;
SELECT * FROM payees;
SELECT * FROM categories;
