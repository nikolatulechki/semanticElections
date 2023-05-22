# semanticElections

RDF-ization of Bulgarian election results

# Data transformation pipeline

## CIK open data 

The main data source is the open data package published by CIK after each election.
These are in a non normalized tabular format and require the following transformation steps:

- download and unzipping in local storage. This is currrently done manually and te results are in [cikOpenData](../gdrive/data/cikOpenData), corresponding to [this](https://drive.google.com/drive/folders/1ZyNu9THMCS5aP0N68iqvBIE0X1fsDDYP?usp=share_link) GFolder
- removal of some quotes ([dequote.sh](dequote.sh)) 
- verticalization of the `votes.txt` file, done with [flatten.sh](flatten.sh), the pattern changes for each election cycle 
- summing op of votes. This is an ugly hack to ensure data consistency - [sum_votes.sh](sum_votes.sh) sums  up votes from different machines in the same section in order to have a single number in the final data
- transformation to rdf with custom or generic Tarql scripts. This is currently orchestrated by a python script such as [transform_pi2023.py](transform_pi2023.py)
- [TODO] we should rewrite all the transformations to use Ontotext Refine

## Additional data from Google Sheets

- mappings and correspondence tables are kept in google sheets as a primary data store. This allows us to edit individual values and assure data interoperability between election cycles, by for example mapping party identifiers (ballot numbers) to a main party object (wikidata identifier)
- they are consumed live as csv and then transformed to RDF using the associated Tarql scripts. see [get-google-sheets.sh](get-google-sheets.sh) and [make_mappings.py](make_mappings.py)

## Static data sources

- Static data is stored in the repository, either in CSV or RDF format in [static](static)
- The CSVs are transformed using Tarql, the RDF is used as-is.

## Data import into GDB

- After all the transformation processes are completed they are imported in a GDB repository 
- [TODO - add to giit]  a script collects all the RDF files from the [rdf](rdf) and [rdf](static/rdf) folders and moves them to the GDB data import directory. 
- They are then imported manually using the UI.
- [TODO] This is wildly suboptimal. We should rewrite this to use the GDB REST api and store the triples in dedicated named graphs and not in default graph.

## Inference 

- After all the rdf is imported into GDB, a number of SPARQL scripts ran against the repository to create more connections and facts.
- These are in [sparql](sparql) and are executed by hand in the filename order. 
- [TODO] We should automate this and run the scripts using the REST api 




