select 
    id,
    cast(transaction_date as char),
    customer_id
from henry.transactions
where transactions.transaction_date = '{{ date }}'


