SELECT * FROM goods
WHERE price = (SELECT (max(price)) FROM goods)