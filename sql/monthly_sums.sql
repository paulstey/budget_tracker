SELECT sum(amount), category, YEAR(date_purchased), MONTH(date_purchased)
  FROM purchases
 GROUP BY category, YEAR(date_purchased), MONTH(date_purchased)
 ORDER BY category, YEAR(date_purchased), MONTH(date_purchased);
