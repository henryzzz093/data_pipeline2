create schema henry;

create table if not exists henry.stocks (
    date date,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    adj_close numeric,
    volume int
);