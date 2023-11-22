# Senior-Capstone
# Clear Database
```cypher
SHOW DATABASES
```
```CREATE OR REPLACE DATABASE neo4j```
# Load Database ( Order Matters )
```
// Create Servers nodes
LOAD CSV WITH HEADERS FROM "file:///Servers.csv" AS row
CREATE (:Server {
    Name: row.Name,
    OS: row.OS,
    DataCenter: row.DataCenter,
    IsVirtual: row.IsVirtual,
    ParentServer: row.ParentServer
});
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

// Load CSV and create Applications nodes with HOSTS_APP relationship to Server nodes
LOAD CSV WITH HEADERS FROM "file:///Applications.csv" AS row
CREATE (a:Application {
    Name: row.Name,
    Description: row.Description
})
WITH a, row
UNWIND split(row.Servers, ": ") AS serverID
MATCH (srv:Server {Name: serverID})
MERGE (a)-[:HOSTS_APP]->(srv);

LOAD CSV WITH HEADERS FROM "file:///Incidents.csv" AS row
MERGE (srv:Server {Name: row.AffectedServer}) 
CREATE (inc:Incident {
    ID: row.ID,
    Severity: row.Severity,
    ReportedDate: row.ReportedDate,
    Description: row.Description,
    AffectedServer: row.AffectedServer
})
MERGE (inc)-[:AFFECTS_SERVER]->(srv);

// Create DataCenters nodes
LOAD CSV WITH HEADERS FROM "file:///DataCenters.csv" AS row
CREATE (:DataCenter {
    Name: row.Name,
    State: row.State,
    City: row.City
});

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
