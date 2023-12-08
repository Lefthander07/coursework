SELECT goods.idgoods, gname
FROM buyers join orders
on buyers.idbuyers = orders.idbuyer join order_line
on orders.idorders = order_line.idorder join goods
on order_line.idgoods = goods.idgoods
WHERE name = '$bname' and YEAR(payment_date) = $year
and MONTH(payment_date) = $month
GROUP BY goods.idgoods