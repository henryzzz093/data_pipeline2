select 
    transaction_details.id,
    transaction_id,
    product_id,
    quantity
from henry.transaction_details
left join henry.transactions on transaction_details.transaction_id = transactions.id
where transactions.transaction_date = '{{ date }}'


