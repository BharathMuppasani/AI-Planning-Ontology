from calendar import c
from cmath import e
from itertools import count
from rdflib import *
from rdflib import Namespace
from rdflib.term import URIRef, Literal
from rdflib.plugins import sparql
from rdflib.namespace import RDF, RDFS, OWL
import json


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



g = Graph().parse('./models/plan-ontology-rdf-instances_test.owl')
planningOntology = Namespace('https://purl.org/ai4s/ontology/planning#')

data_file_path = "data/planner_data_test.json"

f = open(data_file_path)
data = json.load(f)


for domain_instance in data.keys():
   domain_URI = URIRef(planningOntology + domain_instance.replace(' ','-'))
   for relevance in data[domain_instance].keys():
      if relevance == 'high':
         property_URI = URIRef(planningOntology + 'hasHighRelevancePlanner')
      elif relevance == 'medium':
         property_URI = URIRef(planningOntology + 'hasMediumRelevancePlanner')
      elif relevance == 'low':
         property_URI = URIRef(planningOntology + 'hasLowRelevancePlanner')
         
      for planner_instance in data[domain_instance][relevance]:
         planner_instance = planner_instance.replace(' ', '_')
         planner_URI = URIRef( planningOntology + planner_instance )
         g.add((planner_URI, RDF.type, planningOntology.Planner))
         g.add((planner_URI, RDFS.label, Literal(planner_instance)))
         g.add((domain_URI, property_URI, planner_URI))
   

g.serialize(destination="./models/plan-ontology-rdf-instances-planner-info_test.owl", format="xml")

