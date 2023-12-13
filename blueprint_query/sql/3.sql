SELECT * FROM goods
WHERE price = (SELECT ($minmax(price)) FROM goods)