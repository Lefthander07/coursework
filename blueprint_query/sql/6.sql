SELECT * FROM (SELECT idbuyers, name, address, contact_number,  BIC, account_number,  bank, conclusion_date, COUNT(*) as countt FROM buyers join orders on buyers.idbuyers = orders.idbuyer
WHERE status = 1 AND YEAR(order_date) = $date
GROUP by idbuyers) o21 WHERE countt = (SELECT MAX(countt) from (SELECT idbuyers, name, address, contact_number,  BIC, account_number,  bank, conclusion_date,COUNT(*) as countt FROM buyers join orders on buyers.idbuyers = orders.idbuyer
WHERE status = 1 and YEAR(order_date) = $date
GROUP by idbuyers) as o20)