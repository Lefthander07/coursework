SELECT idgoods,gname,order_line.quantity, price from order_line join goods using(idgoods)
WHERE idorder = $idorder