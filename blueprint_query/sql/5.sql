SELECT buyers.* FROM buyers LEFT join (SELECT idbuyer as idbuyers, idorders
FROM orders WHERE year(payment_date)=$year and month(payment_date) = $month) o20 using (idbuyers)
WHERE idorders is NULL