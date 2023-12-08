SELECT buyers.* FROM buyers JOIN orders using(idbuyers)
WHERE purchases_2020.count_order = (SELECT MAX(count_order) FROM purchases_2020)