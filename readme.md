## Class 12 CS Project

This is the CS project that I made for class 12.

## Note:

Change the user and password for MySQL in python file

## Set Up MySQL Table.

```sql
CREATE DATABASE expense_tracker;

USE expense_tracker;

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    type VARCHAR(10) NOT NULL,  -- 'income' or 'expense'
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL
);

```

## Install Python Libraries

```bash
pip install inquirer
```
