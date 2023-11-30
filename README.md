# Senior-Capstone
# 1. Install Requirements
```bash
pip3 install faker==19.8.0
```
# 2. Build Script
```bash
./build.sh
```
> This will alias python3  to virtual env if present  
> Then run python3 files, generating CSVs  
> Please note that servers.txt must persist and be present in current working directory until all other CSVs are generated  
# 3. Neo4j Queries
## 3.1 Clear Database
```cypher
SHOW DATABASES
```  

```cypher
CREATE OR REPLACE DATABASE neo4j
```
## 3.2 Constraints
```cypher
CREATE CONSTRAINT FOR (s:Server) REQUIRE s.Name IS UNIQUE;
CREATE CONSTRAINT FOR (i:Incident) REQUIRE i.ID IS UNIQUE;
CREATE CONSTRAINT FOR (c:ChangeRecord) REQUIRE c.ID IS UNIQUE;
CREATE CONSTRAINT FOR (a:Application) REQUIRE a.Name IS UNIQUE;
```
## 3.3 Load Database ( Order Matters )
```cypher
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

### 3.4 Date Based Queries 
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

### 3.5 Change Based Queries
**3.5.1 Get Server Affected By Change**  

```
MATCH (c:Change{ID:"CHG-086632"})-[AFFECTS_SERVER]-(s)
return c,s
```
**3.5.2 Get Servers Affected By Change**
```cypher
MATCH (c:Change)-[AFFECTS_SERVER]-(s)
return c,s
LIMIT 25
```

**3.5.3 Get Servers Affected By a Change in a certain date range** ( based off of epoch time)
```cypher
MATCH (change:Change)
WHERE datetime({epochSeconds: toInteger(change.StartEpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(change.StartEpochTime)}) <= datetime('2023-12-31T23:59:59Z')
with change
match (change)-[AFFECTS_SERVER]-(s:Server)
return change,s
LIMIT 100
```
### 3.6Application Based Queries 
**3.6.1 See all which apps are hosted on what servers**  
```cypher
match (a:Application)-[HOSTS_APP]-(s:Server)
return a,s
LIMIT 25
```

**3.6.2 See all apps with a description and which server it is hosted on**  
```cypher
MATCH (a:Application{Description: "empower synergistic markets"})-[HOSTS_APP]->(s)
return a,s
LIMIT 25
```


**3.6.3 See which servers a specific app is running on** ( textual )  
```cypher
match (a:Application{Name:"APP-07851"})-[HOSTS_APP]-(s:Server)
return a,s
LIMIT 25
```


**3.6.4 See if an application is running on a Windows Server**  
```cypher
match (a:Application{Name:"APP-07851"})-[HOSTS_APP]-(s:Server{OS:"Windows"})
return a,s
LIMIT 25
```


**3.6.5 See the parent servers of a specific application**(as text)    
```cypher
match (a:Application{Name:"APP-07851"})-[HOSTS_APP]-(s:Server)
where s.IsVirtual =  "Yes" 
match (real:Server{Name:s.ParentServer})
return real.Name
```
**3.6.6 Get the changes that are affecting servers which are hosting apps**  
```cypher
MATCH (a:Application)-[HOSTS_APP]->(s:Server)
match (s)-[AFFECTS_SERVER]-(c:Change)
return a,s,c
LIMIT 25
```


**3.6.7 Get the changes that are affecting servers which are hosting apps based on a changes date range**  
```cypher
MATCH (a:Application)-[HOSTS_APP]->(s:Server)
match (s)-[AFFECTS_SERVER]-(c:Change)
MATCH (c:Change)
WHERE datetime({epochSeconds: toInteger(c.StartEpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(c.StartEpochTime)}) <= datetime('2023-12-31T23:59:59Z')
return a,s,c
```
**3.6.8 Get the changes that are affecting servers hosting a specific application(with a name) based off of a date range**
```cypher
MATCH (a:Application{Name:"APP-07270"})-[HOSTS_APP]->(s:Server)
match (s)-[AFFECTS_SERVER]-(c:Change)
MATCH (c:Change)
WHERE datetime({epochSeconds: toInteger(c.StartEpochTime)}) >= datetime('2023-01-01T00:00:00Z')
  AND datetime({epochSeconds: toInteger(c.StartEpochTime)}) <= datetime('2023-12-31T23:59:59Z')
return a,s,c
```
### 3.7 Server Queries
```cypher
match (p:Server)-[:IS_PARENT]-(s:Server)
return p,s
LIMIT 50
```
### 3.8 Incident Queries
```cypher
MATCH (inc:Incident)-[:AFFECTS_SERVER]->(srv:Server)
RETURN inc, srv
Limit 25
```
### 3.9 Datacenter Queries
**3.9.1 Get the datacenter for an application was hosted on Window servers which were affected by incidents**
```cypher
match (a:Application{Name:"APP-07270"})-[:HOSTS_APP]-(s:Server{OS:"Windows"})
match (s)-[AFFECTS_SERVER]-(i:Incident)
match (s)-[LOCATED_IN]-(dc:DataCenter)
return a,s,i,dc
```
**3.9.2 Get the datacenter for an application hosted on a server that was impacted by a High Severity Incident**
```cypher
match (a:Application{Name:"APP-07270"})-[:HOSTS_APP]-(s:Server)
match (s)-[AFFECTS_SERVER]-(i:Incident{Severity:"1-High"})
match (s)-[LOCATED_IN]-(dc:DataCenter)
return a,s,i,dc
```  
**3.9.3 Get the applications affected by a high severity incident after a certain date**
```cypher
match (s:Server)-[AFFECTS_SERVER]-(i:Incident{Severity:"1-High"})
WHERE datetime({epochSeconds: toInteger(i.EpochTime)}) >= datetime('2022-05-01T00:00:00Z') 
match (s)-[:HOSTS_APP]-(a:Application)
return a,s,i
```
# 4. Neo4J Memory Setttings
Below are the changes made to Neo4J settings to handle full dataset ingestion.
```
#********************************************************************
# Memory Settings
#********************************************************************
#
# Memory settings are specified kibibytes with the 'k' suffix, mebibytes with
# 'm' and gibibytes with 'g'.
# If Neo4j is running on a dedicated server, then it is generally recommended
# to leave about 2-4 gigabytes for the operating system, give the JVM enough
# heap to hold all your transaction state and query context, and then leave the
# rest for the page cache.

# Java Heap Size: by default the Java heap size is dynamically calculated based
# on available system resources. Uncomment these lines to set specific initial
# and maximum heap size.
server.memory.heap.initial_size=8g
server.memory.heap.max_size=8g

# The amount of memory to use for mapping the store files.
# The default page cache memory assumes the machine is dedicated to running
# Neo4j, and is heuristically set to 50% of RAM minus the Java heap size.
server.memory.pagecache.size=10g

# Limit the amount of memory that all of the running transaction can consume.
# The default value is 70% of the heap size limit.
dbms.memory.transaction.total.max=0

# Limit the amount of memory that a single transaction can consume.
# By default there is no limit.
db.memory.transaction.max=0
#********************************************************************
# Other Neo4j system properties
#********************************************************************
dbms.memory.heap.initial_size=8G
dbms.memory.heap.max_size=8G
dbms.memory.pagecache.size=10G
```
