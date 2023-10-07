# BoA-Capstone
# Cog Integration

Cog is a 'Micro' Graph Database meaning its simple and concise, if 
# Features of Cog
## Simplicity
Known as an _RDF Database_ [Learn More about RDFs](https://www.w3.org/TR/rdf-concepts/#:~:text=An%20RDF%20triple%20contains%20three,literal%20or%20a%20blank%20node), Data is modelled as  **Vertex Edge Vertex** / **Subject Predicate Object**  
The RDF format is also known as **Triples** and differs from *Neo4j*'s **Property Graph** which allows for greater data encoding.

This means that mapping directional relationships,  
For example,
> the _Application_ which caused an *Incident* on a *Server* for a given *Data Center*  

can be easily managed. But the addition of extra metadata such as time cannot be practically built into Cog's RDF model.  
This simplicity means that the query language is much simpler but so is the data modelling potential.  

***Additionally***,  
self-referencial relationships are not allowed in Cog or any RDF for that matter as the **Subject** and the **Object** in a given relationship must not be the same entity.
## External Format Support
### JSON Support  
```python
f = Graph("followers")
f.putj('{"name" : "bob", "status" : "cool_person", "follows" : ["fred", "dani"]}')
f.putj('{"_id":  "1", "name" : "fred", "status" : "cool_person", "follows" : ["alice", "greg"]}')
```
Cog can utilize JSON in order to map relations between nodes  

### CSV Support 
## Nested Edges
## Properties
## Database Views
Graphs built within code have the ability to build views to render them.
## Resources
[Cog Wiki](https://arun1729.github.io/cog/)
