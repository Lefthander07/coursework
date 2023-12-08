SELECT buyers.* from buyers LEFT join orders on
buyers.idbuyers = orders.idbuyer WHERE idorders is NULL