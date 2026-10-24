


For Task B, we need to make mathematical equation. For SELECT * FROM maint_job WHERE technician = 'Beier'; command, Logic and sequanece should be like this: sigma technician (because we select from WHERE? from technician) equals 'Beier' is text value and (maint\_job) means this means we are doing filtering to the main_job table
$\sigma_{technician='Beier'}(maint\_job)$

LLM Comparison: I asked Gemini to translate the same query. We completely agreed on using the selection operator ($\sigma$) for the WHERE clause. The only difference in our approach was a minor learning point: the LLM pointed out that the projection operator ($\pi$) is usually omitted entirely when the SQL query uses SELECT *.

