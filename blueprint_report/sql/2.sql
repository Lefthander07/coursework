SELECT name, bank, concl_date, spent
FROM report_buyers WHERE 1=1 AND from_date = '$date_from' AND to_date = '$date_to'