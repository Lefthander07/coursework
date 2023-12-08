SELECT idorders, order_date, status,total,payment_date FROM orders
WHERE idbuyer = $user_id