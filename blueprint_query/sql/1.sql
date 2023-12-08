SELECT idbuyers, name, gname, sum(order_line.quantity)
FROM (buyers join orders
on buyers.idbuyers = orders.idbuyer) join order_line
on orders.idorders = order_line.idorder join goods
on order_line.idgoods = goods.idgoods
WHERE 1=1 AND
YEAR(payment_date) = $year and
MONTH(payment_date) = $month
GROUP by idbuyers, gname
