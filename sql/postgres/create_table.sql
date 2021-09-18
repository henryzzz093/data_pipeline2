CREATE SCHEMA IF NOT EXISTS henry;

CREATE TABLE IF NOT EXISTS henry.stocks (
    id serial,
    date date,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    adj_close numeric,
    volume int
);

