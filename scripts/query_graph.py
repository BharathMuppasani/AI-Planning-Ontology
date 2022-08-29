from unittest import result
from numpy import var
from rdflib import *
from rdflib import Namespace
from rdflib.term import URIRef
from rdflib.plugins import sparql
from rdflib.namespace import RDF, RDFS, OWL
from regex import P
from uritemplate import variables

def graph_query(sql_query, g, namespace):
    
    list = sql_query.split('\n')

    for line in list:
        if 'PREFIX' in line or 'PREFIX'.lower() in line:
            prefix_list = [ x for x in line.split(" ") if x]
            dict = {}
            dict[prefix_list[1].replace(':','')] = Namespace(prefix_list[-1].replace('<','').replace('>',''))
            locals().update(dict)
    
    variables = []
    for line in list:
        if 'SELECT' in line or 'SELECT'.lower() in line:
            temp_list = line.split(" ")
            for item in temp_list:
                if '?' in item:
                    variables.append(item.replace('?','').rstrip())
    
    new_query_list = []
    for line in list:
        if 'PREFIX' in line or 'PREFIX'.lower() in line:
            continue
        new_query_list.append(line)
    
    new_query = '\n'.join(new_query_list)
    results = g.query(new_query)
    
    if namespace == None:
        output_dict = {}
        for output in results:
            for idx in range(len(output)):
                if output[idx] != None:
                    if variables[idx] not in output_dict:
                        output_dict[variables[idx]] = [output[idx].split("#")[-1]]
                    else:
                        output_dict[variables[idx]].append(output[idx].split("#")[-1])
    else:
        output_dict = {}
        for output in results:
            for idx in range(len(output)):
                if variables[idx] not in output_dict:
                    output_dict[variables[idx]] = [output[idx]]
                else:
                    output_dict[variables[idx]].append(output[idx])

    all_headers = output_dict.keys()
    all_rows = zip(*output_dict.values())
    
    return all_headers,all_rows
            

