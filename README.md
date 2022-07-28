# AI-Planning-Ontology
A usable planning ontology and its usage in a broad set of planning datasets (IPC)

Contents:
1. *data* - contains the JSON representation of the IPC2018 domain data.
2. *images* - contains images of ontology and sample Knowledge Graph (KG).
3. *models* - contains RDF/OWL files of the ontology and the associated knowledge graph.
4. *queries* - contains .docx file with sample SPARQL queries performed on the KG and their results.
5. *scripts* - contains the scripts required 
    - get_data.py - to build the JSON data file of the IPC domains from the location specified as command line argument.
        > python3 get_data.py <\folder_path>
    - infuse.py - to infuse the data from JSON file into the ontology based on the relations between different entities.
        > python3 infuse.py

To run the website on localhost, please install Flask and run
    > python3 .\scripts\website.py
