from rdflib import *
from rdflib import Namespace
from rdflib.term import URIRef
from rdflib.plugins import sparql
from rdflib.namespace import RDF, RDFS, OWL

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

g = Graph().parse('./models/plan-ontology-rdf.owl')
planOntology = Namespace('http://www.semanticweb.org/muppa/ontologies/2022/4/plan-ontology#')

print("Number of Triples in the Graph: ",len(g),end="\n\n")

