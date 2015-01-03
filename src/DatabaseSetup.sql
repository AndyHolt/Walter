-- File name: Walter/src/DatabaseSetup.sql
-- Set up tables and data types for Walter databse.
-- Author: adh
-- Date: Sat 03 Jan 2015 13:34

-- select the Walter database
-- [todo] - allow selection of test database instead
USE walter_dev;

-- create payees table
-- (must be done before transactions for foreign key assignment)
CREATE TABLE IF NOT EXISTS payees
       (payee_id SERIAL PRIMARY KEY,
        payee_name VARCHAR(100)
);

-- create transactions table
CREATE TABLE IF NOT EXISTS transactions
       (transaction_id SERIAL PRIMARY KEY,
        date DATE,
        payee_id BIGINT UNSIGNED NOT NULL,
        description VARCHAR(100),
        amount DECIMAL(10,2),

        CONSTRAINT tr_pa_fk
        FOREIGN KEY fk_payee(payee_id)
        REFERENCES payees(payee_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- create categories table
-- [review] - does self referencing FK work on UPDATE?
CREATE TABLE IF NOT EXISTS categories
       (category_id SERIAL PRIMARY KEY,
        parent_id BIGINT UNSIGNED,
        category_name VARCHAR(100),

        CONSTRAINT cat_parent_fk
        FOREIGN KEY fk_cat_parent(parent_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- create transaction_items table
CREATE TABLE IF NOT EXISTS transaction_items
       (transaction_item_id SERIAL PRIMARY KEY,
        transaction_id BIGINT UNSIGNED NOT NULL,
        description VARCHAR(100),
        amount DECIMAL(10,2),
        category_id BIGINT UNSIGNED NOT NULL,

        CONSTRAINT trit_tr_fk
        FOREIGN KEY fk_transactions(transaction_id)
        REFERENCES transactions(transaction_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

        CONSTRAINT trit_cat_fk
        FOREIGN KEY fk_categories(category_id)
        REFERENCES categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
