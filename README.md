# Senior-Capstone

Useful Queries:
// retrieve Incidents within a timeframe
MATCH (incident:Incident)
WHERE datetime({epochSeconds: toInteger(incident.EpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(incident.EpochTime)}) <= datetime('2023-12-31T23:59:59Z')
RETURN incident;

// retrive Changes within a timeframe
MATCH (change:Change)
WHERE datetime({epochSeconds: toInteger(change.StartEpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(change.StartEpochTime)}) <= datetime('2023-12-31T23:59:59Z')
RETURN change;

// counts number of incidents per month
MATCH (incident:Incident)
WITH incident, datetime({epochSeconds: toInteger(incident.EpochTime)}) AS incidentDate
RETURN date(incidentDate).month as month, COUNT(incident) as incidentCount
ORDER BY month;

// counts number of changes per month
MATCH (change:Change)
WITH change, date(datetime({epochSeconds: toInteger(change.StartEpochTime)})) AS changeDate
RETURN changeDate.year AS year, changeDate.month AS month, COUNT(change) AS changeCount
ORDER BY year, month;
