# AI-Planning-Ontology
A usable planning ontology and its usage in a broad set of planning datasets (IPC)

PyLODE Documentation of the Ontology - [Click Here][https://raw.githack.com/BharathMuppasani/AI-Planning-Ontology/main/ontology_documentation.html]

Contents:
1. *data* - contains the JSON representation of the IPC2018 domain data.
2. *images* - contains images of ontology and sample Knowledge Graph (KG).
3. *models* - contains RDF/OWL files of the ontology and the associated knowledge graph.
4. *queries* - contains .docx file with sample SPARQL queries performed on the KG and their results.
5. *scripts* - contains the scripts required 
    - get_data.py - to build the JSON data file of the IPC domains from the location specified as command line argument.
        > python3 .\script\get_data.py <\folder_path>
    - infuse.py - to infuse the data from JSON file into the ontology based on the relations between different entities.
        > python3 .\script\infuse.py

To run the website on localhost, please install Flask and run the following command:
> python3 .\scripts\website.py


# Citations
If you are using our work, please cite.
```
@inproceedings{planning-ontology,

author = {Bharath Muppasani and Vishal Pallagani  and Biplav Srivastava  and Raghava Mutharaju},

title = {Building and using a planning ontology from past data for performance efficiency},

booktitle = {Proc. ICAPS'23 Workshop PLanning And onTology wOrkshop (PLATO)},
year = {2023},
keywords = {  Ontology, Automated Planning, Planner Improvement},
copyright = {Creative Commons Attribution Non Commercial No Derivatives 4.0 International}

}
```
