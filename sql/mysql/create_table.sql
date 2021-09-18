
CREATE TABLE IF NOT EXISTS henry.stocks (
    id int AUTO_INCREMENT,
    date date,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    adj_close numeric,
    volume int,
    PRIMARY KEY (id)
);

