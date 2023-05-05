from asyncio import constants
import numpy as np
import os
import sys
import glob
import json
import re
import domain_functions as df
import problem_functions as pf


def write_to_json(data,path):

    json_object = json.dumps(data,indent=4)

    # writing dictionary data into json file
    with open(path,"w") as out:
        out.write(json_object)

def search_file(file_path,string):
    with open(file_path, 'r') as f:
        line_number = 0
        for line in f:
            if string in line or string.upper() in line:
                return line_number
            line_number += 1
    
    return -1


data_file_path = "data.json"

f = open(data_file_path)
data = json.load(f)

file_path = sys.argv[1]
domain_files = []
problem_files = []

for f in glob.iglob(file_path + '/**/*.pddl', recursive=True):
    if search_file(f,'(:goal') == -1 :
        domain_files.append(f)
    else:
        problem_files.append(f)


for file in domain_files:
    name = df.get_domain_name(file).strip()

    str_file = open(file).read()

    if '(:requirements' in str_file:
        requirements = df.get_requirements(file)
    else:
        requirements = []

    if '(:types' in str_file:
        types = df.get_types(file)
    else:
        types = {}

    if '(:constants' in str_file:
        constants = df.get_constants(file)
    else:
        constants = {}

    if '(:predicates' in str_file:
        predicates = df.get_predicates(file)
    else:
        predicates = []

    if '(:action' in str_file:
        actions = df.get_actions(file)
    else:
        actions = {}

    if name not in data.keys():
        print("Adding ",name," domain file")
        data[name] = {}
        data[name]["requirements"] = requirements
        data[name]["types"] = types
        data[name]["constants"] = constants
        data[name]["predicates"] = predicates
        data[name]["actions"] = actions

for file in problem_files:
    problem_name, domain_name = pf.get_problem_name(file)

    problem_name = problem_name.strip()
    domain_name = domain_name.strip()

    str_file = open(file).read()

    if '(:objects' in str_file:
        objects = pf.get_objects(file)
    else:
        objects = []

    if '(:init' in str_file:
        init = pf.get_initialState(file)
    else:
        init = {}

    if '(:goal' in str_file:
        goal = pf.get_goalState(file)
    else:
        goal = []

    if domain_name not in data.keys():
        print("Adding ",problem_name," problem file for ",domain_name," domain file")
        data[domain_name] = {}
        data[domain_name]["Problems"] = {}
        data[domain_name]["Problems"][problem_name] = {}
        data[domain_name]["Problems"][problem_name]["objects"] = objects
        data[domain_name]["Problems"][problem_name]["init"] = init
        data[domain_name]["Problems"][problem_name]["goal"] = goal
    else:
        print("Adding ",problem_name," problem file for ",domain_name," domain file")
        if "Problems" not in data[domain_name].keys():
            data[domain_name]["Problems"] = {}
            data[domain_name]["Problems"][problem_name] = {}
            data[domain_name]["Problems"][problem_name]["objects"] = objects
            data[domain_name]["Problems"][problem_name]["init"] = init
            data[domain_name]["Problems"][problem_name]["goal"] = goal
        else:
            data[domain_name]["Problems"][problem_name] = {}
            data[domain_name]["Problems"][problem_name]["objects"] = objects
            data[domain_name]["Problems"][problem_name]["init"] = init
            data[domain_name]["Problems"][problem_name]["goal"] = goal

write_to_json(data,data_file_path)
