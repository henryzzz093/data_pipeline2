select 
    customers.id, 
    name, 
    address, 
    phone, 
    email
from henry.customers 
left join henry.transactions on customers.id = transactions.customer_id
where transactions.transaction_date = '{{ date }}'


