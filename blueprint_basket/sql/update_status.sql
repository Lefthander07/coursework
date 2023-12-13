UPDATE orders SET status = 1, payment_date = CURDATE()
WHERE idorders = $idorder