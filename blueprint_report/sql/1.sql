SELECT idgoods , gname , quantity,
 total
 FROM report_goods WHERE 1=1 AND from_date = '$date_from' AND to_date = '$date_to'