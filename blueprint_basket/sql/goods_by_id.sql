SELECT
    *
FROM goods
WHERE 1=1
    AND idgoods IN ($goods_ids)