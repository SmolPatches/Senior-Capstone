# Senior-Capstone
# Clear Database
```cypher
SHOW DATABASES
```
```CREATE OR REPLACE DATABASE neo4j```
# Load Database ( Order Matters )
```
// Load CSV and create Change nodes with AFFECTS_SERVER relationship to Server nodes
LOAD CSV WITH HEADERS FROM "file:///Changes.csv" AS row
CREATE (chg:Change {
    ID: row.ID,
    StartDate: row.StartDate,
    EndDate: row.EndDate,
    Description: row.Description
})
WITH chg, row
UNWIND split(row.AffectedServer, ":") AS serverID
MATCH (srv:Server {Name: serverID})
MERGE (chg)-[:AFFECTS_SERVER]->(srv);
```

## Date Based Queries 
```cypher
// Retrieve Incidents within a Timeframe
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
```
