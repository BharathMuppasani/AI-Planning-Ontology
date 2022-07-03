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

def get_class_name( input_string ):

   if input_string == 'requirements':
      return planOntology.requirement, planOntology.hasRequirement
   elif input_string == 'types':
      return planOntology.type, planOntology.hasType
   elif input_string == 'constants':
      return planOntology.constant, planOntology.hasConstant
   elif input_string == 'predicates':
      return planOntology.predicate, planOntology.hasPredicate
   elif input_string == 'actions':
      return planOntology.action, planOntology.hasMove
   elif input_string == 'Problems':
      return planOntology.problem, planOntology.hasProblem

def add_requirements( class_name, property_name, itemURI, data ):
   if type(data) is list:
      for value in data:
         value_URI = URIRef( planOntology + value )
         g.add((value_URI, RDF.type, class_name))
         g.add((value_URI, RDFS.label, Literal(value)))
         g.add((itemURI, property_name, value_URI))


def add_types( class_name, property_name, itemURI, data ):
   if type(data) is list:
      for value in data:
         value_URI = URIRef( planOntology + value )
         g.add((value_URI, RDF.type, class_name))
         g.add((value_URI, RDFS.label, Literal(value)))
         g.add((itemURI, property_name, value_URI))

   elif type(data) is dict:
      if len(data.keys()) > 1:
         for tag in data.keys():
            tag_URI = URIRef( planOntology + tag )
            g.add((tag_URI, RDF.type, planOntology.type_tag))
            g.add((tag_URI, RDFS.label, Literal(tag)))
            for value in data[tag]:
               value_URI = URIRef( planOntology + value )
               g.add((value_URI, RDF.type, class_name))
               g.add((value_URI, RDFS.label, Literal(value)))
               g.add((itemURI, property_name, value_URI))
               g.add((value_URI, planOntology.hasTag, tag_URI))


def add_constants( class_name, property_name, itemURI, data ):
   if type(data) is list:
      for value in data:
         value_URI = URIRef( planOntology + value )
         g.add((value_URI, RDF.type, class_name))
         g.add((value_URI, RDFS.label, Literal(value)))
         g.add((itemURI, property_name, value_URI))

   elif type(data) is dict:
      if len(data.keys()) > 1:
         for tag in data.keys():
            for value in data[tag]:
               value_URI = URIRef( planOntology + value )
               g.add((value_URI, RDF.type, class_name))
               g.add((value_URI, RDFS.label, Literal(value)))
               g.add((itemURI, property_name, value_URI))


def add_predicates( class_name, property_name, itemURI, data ):
   count = 0
   for value in data:
      count += 1
      value_URI = URIRef( planOntology +  itemURI.split('#')[-1] + '_predicate_' + str(count) )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(value)))
      g.add((itemURI, property_name, value_URI))
   

def add_parameters( class_name, property_name, itemURI, data):
   if len(data["values"]) == len(data["types"]):

      for idx in range(len(data["values"])):
         value_URI = URIRef( planOntology + data["values"][idx] )
         type_URI = URIRef( planOntology + data["types"][idx] )
         g.add((value_URI, RDF.type, class_name))
         g.add((value_URI, RDFS.label, Literal(data["values"][idx])))

         g.add((type_URI, RDF.type, planOntology.type))
         g.add((type_URI, RDFS.label, Literal(data["types"][idx])))

         g.add((value_URI, planOntology.ofType, type_URI))
         g.add((itemURI, property_name, value_URI))
   else:
      for idx in range(len(data["values"])):
         value_URI = URIRef( planOntology + data["values"][idx] )
         g.add((value_URI, RDF.type, class_name))
         g.add((value_URI, RDFS.label, Literal(data["values"][idx])))
         g.add((itemURI, property_name, value_URI))

def add_preconditions( class_name, property_name, itemURI, data ):
   count = 0
   for value in data:
      count += 1
      value_URI = URIRef( planOntology + itemURI.split('#')[-1] + '_precondition_' + str(count) )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(value)))
      g.add((itemURI, property_name, value_URI))

def add_effects( class_name, property_name, itemURI, data ):
   count = 0
   for value in data:
      count += 1
      value_URI = URIRef( planOntology + itemURI.split('#')[-1] + '_effect_' + str(count) )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(value)))
      g.add((itemURI, property_name, value_URI))



def add_actions( class_name, property_name, itemURI, data ):
   for action in data.keys():
      value_URI = URIRef( planOntology + action )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(action)))
      g.add((itemURI, property_name, value_URI))
      for item in data[action]:

         if item == 'parameters':
            add_parameters( planOntology.parameter, planOntology.hasParameter, value_URI, data[action][item] )

         if item == 'preconditions':
            add_preconditions( planOntology.precondition, planOntology.hasPrecondition, value_URI, data[action][item] )

         if item == 'effect':
            add_effects( planOntology.effect, planOntology.hasEffect, value_URI, data[action][item] )
   

def add_objects( class_name, property_name, itemURI, domain_name, data ):
   if type(data) is dict:
      count = 0
      for item_type in data.keys():
         type_URI = URIRef( planOntology + item_type )
         g.add(( type_URI, RDF.type, planOntology.type ))
         g.add(( type_URI, RDFS.label, Literal(item_type)))
         g.add(( URIRef(planOntology + domain_name), planOntology.hasType, type_URI ))
         for value in data[item_type]:
            count += 1
            value_URI = URIRef( planOntology + value)
            g.add((value_URI, RDF.type, class_name))
            g.add((value_URI, RDFS.label, Literal(value)))
            g.add((itemURI, property_name, value_URI))
            g.add((type_URI, planOntology.hasTypeInstance, value_URI))
   elif type(data) is list:
      count = 0
      for value in data:
         count += 1
         value_URI = URIRef( planOntology + value)
         g.add((value_URI, RDF.type, class_name))
         g.add((value_URI, RDFS.label, Literal(value)))
         g.add((itemURI, property_name, value_URI))   


def add_initial_state( class_name, property_name, itemURI, data):
   count = 0
   for value in data:
      count += 1
      value_URI = URIRef( planOntology + itemURI.split('#')[-1] + '_initial_state_' + str(count) )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(value)))
      g.add((itemURI, property_name, value_URI))

def add_goal_state( class_name, property_name, itemURI, data):
   count = 0
   for value in data:
      count += 1
      value_URI = URIRef( planOntology + itemURI.split('#')[-1] + '_goal_state_' + str(count) )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(value)))
      g.add((itemURI, property_name, value_URI))

def add_problem( class_name, property_name, itemURI, data ):
   for problem in data.keys():
      value_URI = URIRef( planOntology + problem )
      g.add((value_URI, RDF.type, class_name))
      g.add((value_URI, RDFS.label, Literal(problem)))
      g.add((itemURI, property_name, value_URI))
      for item in data[problem]:

         if item == 'objects':
            add_objects( planOntology.object, planOntology.hasObject, value_URI, itemURI.split('#')[-1], data[problem][item] )

         if item == 'init':
            add_initial_state( planOntology.initial_state, planOntology.hasInitialState, value_URI, data[problem][item] )

         if item == 'goal':
            add_goal_state( planOntology.goal_state, planOntology.hasGoalState, value_URI, data[problem][item] )

g = Graph().parse('./models/plan-ontology-rdf.owl')
planOntology = Namespace('http://www.semanticweb.org/muppa/ontologies/2022/4/plan-ontology#')

data_file_path = "data/data.json"

f = open(data_file_path)
data = json.load(f)


for domain_instance in data.keys():
   itemURI = URIRef( planOntology + domain_instance )
   g.add((itemURI, RDF.type, planOntology.domain))
   g.add((itemURI, RDFS.label, Literal(domain_instance)))
   for domain_instance_property in data[domain_instance].keys():
      class_name, property_name = get_class_name(domain_instance_property)

      if domain_instance_property == 'requirements':
         add_requirements(class_name, property_name, itemURI, data[domain_instance][domain_instance_property])

      if domain_instance_property == 'types':
         add_types(class_name, property_name, itemURI, data[domain_instance][domain_instance_property])

      if domain_instance_property == 'constants':
         add_constants(class_name, property_name, itemURI, data[domain_instance][domain_instance_property])

      if domain_instance_property == 'predicates':
         add_predicates(class_name, property_name, itemURI, data[domain_instance][domain_instance_property])

      if domain_instance_property == 'actions':
         add_actions(class_name, property_name, itemURI, data[domain_instance][domain_instance_property])

      if domain_instance_property == 'Problems':
         add_problem(class_name, property_name, itemURI, data[domain_instance][domain_instance_property])

g.serialize(destination="./models/plan-ontology-rdf-instances.owl", format="xml")

