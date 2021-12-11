select 
    id,
    cast(transaction_date as char) as transaction_date,
    customer_id
from henry.transactions
where transactions.transaction_date = '{{ date }}'


