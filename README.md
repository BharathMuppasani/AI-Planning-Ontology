# AI-Planning-Ontology
A usable planning ontology and its usage in a broad set of planning datasets (IPC)

Contents:
1. *data* - contains the JSON representation of the IPC2018 domain data.
2. *models* - contains RDF/OWL files of the ontology and the associated knowledge graph.
3. *scripts* - contains the scripts required 
    - data_infuse.py - to build the JSON data file of the IPC domains from the location specified as command line argument.
    > python3 data_infuse.py <\folder_path>