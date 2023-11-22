# Senior-Capstone
# Requirements
```pip install faker==19.8.0```
# Build Script
```./build.sh```
> This will alias python3  to virtual env if present  
> Then run python3 files, generating CSVs
Please note that servers.txt must persist and be present in current working directory until all other CSVs are generated
# Clear Database
```cypher
SHOW DATABASES
```
```CREATE OR REPLACE DATABASE neo4j```
# Constraints
```
CREATE CONSTRAINT FOR (s:Server) REQUIRE s.Name IS UNIQUE;
CREATE CONSTRAINT FOR (i:Incident) REQUIRE i.ID IS UNIQUE;
CREATE CONSTRAINT FOR (c:ChangeRecord) REQUIRE c.ID IS UNIQUE;
CREATE CONSTRAINT FOR (a:Application) REQUIRE a.Name IS UNIQUE;
```
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
    StartEpochTime: row.StartEpochTime, 
    EndEpochTime: row.EndEpochTime,
    Description: row.Description
})
WITH chg, row
UNWIND split(row.AffectedServer, ": ") AS serverID // space after colon is essential
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
    EpochTime: row.EpochTime,
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
// make relation between virtual and physical servers
MATCH (vs:Server {IsVirtual: "Yes"})
MATCH (ps:Server {IsVirtual: "No", Name: vs.ParentServer})
MERGE (vs)-[:IS_PARENT]->(ps);

// connect servers to datacenter 
MATCH (s:Server)
MATCH (dc:DataCenter {Name: s.DataCenter})
MERGE (s)-[:LOCATED_IN]->(dc);
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

## Change Based Queries
**Get Server Affected By Change**
```
MATCH (c:Change{ID:"CHG-086632"})-[AFFECTS_SERVER]-(s)
return c,s
```
**Get Servers Affected By Change**
```
MATCH (c:Change)-[AFFECTS_SERVER]-(s)
return c,s
LIMIT 25
```

**Get Servers Affected By a Change in a certain date range** ( based off of epoch time)
```
MATCH (change:Change)
WHERE datetime({epochSeconds: toInteger(change.StartEpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(change.StartEpochTime)}) <= datetime('2023-12-31T23:59:59Z')
with change
match (change)-[AFFECTS_SERVER]-(s:Server)
return change,s
LIMIT 100
```
## Application Based Queries 
**See all which apps are hosted on what servers**  
```
match (a:Application)-[HOSTS_APP]-(s:Server)
return a,s
LIMIT 25
```

**See all apps with a description and which server it is hosted on**  
```
MATCH (a:Application{Description: "empower synergistic markets"})-[HOSTS_APP]->(s)
return a,s
LIMIT 25
```


**See which servers a specific app is running on** ( textual )  
```
match (a:Application{Name:"APP-07851"})-[HOSTS_APP]-(s:Server)
return a,s
LIMIT 25
```


**See if an application is running on a Windows Server**  
```
match (a:Application{Name:"APP-07851"})-[HOSTS_APP]-(s:Server{OS:"Windows"})
return a,s
LIMIT 25
```


**See the parent servers of a specific application**(as text)    
```
match (a:Application{Name:"APP-07851"})-[HOSTS_APP]-(s:Server)
where s.IsVirtual =  "Yes" 
match (real:Server{Name:s.ParentServer})
return real.Name
```
**Get the changes that are affecting servers which are hosting apps**  
```
MATCH (a:Application)-[HOSTS_APP]->(s:Server)
match (s)-[AFFECTS_SERVER]-(c:Change)
return a,s,c
LIMIT 25
```


**Get the changes that are affecting servers which are hosting apps based on a changes date range**  
```
MATCH (a:Application)-[HOSTS_APP]->(s:Server)
match (s)-[AFFECTS_SERVER]-(c:Change)
MATCH (c:Change)
WHERE datetime({epochSeconds: toInteger(c.StartEpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(c.StartEpochTime)}) <= datetime('2023-12-31T23:59:59Z')
return a,s,c
```
## Server Queries
```
match (p:Server)-[:IS_PARENT]-(s:Server)
return p,s
LIMIT 50
```
## Incident Queries
```
MATCH (inc:Incident)-[:AFFECTS_SERVER]->(srv:Server)
RETURN inc, srv
Limit 25
```