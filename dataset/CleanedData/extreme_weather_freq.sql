SELECT event, count(field1) as alerts_total
FROM districteventList
GROUP by event
HAVING vtec NOTNULL
ORDER by alerts_total DESC