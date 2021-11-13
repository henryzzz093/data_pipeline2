CREATE SCHEMA IF NOT EXISTS henry;

CREATE TABLE IF NOT EXISTS henry.stocks (
    id serial,
    date date,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    adj_close numeric,
    volume int,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP 

);

CREATE TABLE IF NOT EXISTS henry.customers (
    id serial PRIMARY KEY,
    name varchar(50),
    address varchar(200),
    phone varchar(50),
    email varchar(50),
    created_at timestamp DEFAULT CURRENT_TIMESTAMP 
);


