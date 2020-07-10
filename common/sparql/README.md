# QueryUtils
Handles prefixes.
Serializing for queries or turtle as needed.

# Executor
1. Loops through folder and discovers queries to be run.
2. Adds relevant prefixes using QueryUtils
3. Adds clear of the graph and replaces the graph name according
to the query name
4. Executes queries agains a repository

# QueryTest
This object resides in the tests section.
Use it to test update queries in memory.
1. Parses input & expected rdf file
2. Executes insert query on the input data
3. Extracts the result using the graph variable
4. Returns resulting triples and expected triples as
tuple of sorted lists

# QueryFolderTest
A wrapper for QueryTest depends on 3 folders:
* update queries
* input ttl - each update query should have a relevant input (same name + ".ttl")
* output ttl - each update query should have a relevant output (same name + ".ttl")

