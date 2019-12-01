SELECT districtId, state, event, count(field1) as alerts_total
FROM districteventList
GROUP by districtId, event
HAVING vtec NOTNULL