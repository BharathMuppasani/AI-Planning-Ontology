import numpy as np
import os
import sys
import glob
import json

def write_to_json(data,path):

    json_object = json.dumps(data,indent=4)

    # writing dictionary data into json file
    with open(path,"w") as out:
        out.write(json_object)

def find_parens(s):
    toret = {}
    pstack = []
    flag = 0
    for i, c in enumerate(s):

        if flag == 1 and len(pstack) == 0:
            return toret

        if c == '(':
            pstack.append(i)
            flag = 1
        elif c == ')':
            toret[pstack.pop()] = i

    return toret


def search_file(file_path,string):
    with open(file_path, 'r') as f:
        line_number = 0
        for line in f:
            if string in line or string.upper() in line:
                return line_number
            line_number += 1
    
    return -1


def get_domain_name(file):
    with open(file,'r') as f:
        for line in f:
            if '(domain' in line:
                ind = line.index('(domain')
                return line[ind:-1].strip('(domain')[:-1]
            if '(domain'.upper() in line:
                ind = line.index('(domain'.upper())
                return line[ind:-1].strip('(domain'.upper())[:-1]

def get_requirements(file):

    with open(file) as f:
        file_data = f.read()
        requirement_index = file_data.index('(:requirements')
        present_text = file_data[requirement_index:requirement_index + find_parens(file_data[requirement_index:])[0]]

        return present_text.split()[1:]

def get_predicates(file):

    with open(file) as f:
        file_data = f.read()
        predicate_index = file_data.index('(:predicates')
        predicate_closing_ind = find_parens( file_data[predicate_index:] )[0]

        file_data = file_data[predicate_index: predicate_index + predicate_closing_ind+1]

        predicates_list = []
        for ind in range(1, len(file_data)):
            if file_data[ind] == "(":
                # print(ind,file_data[ind])
                closing_ind = find_parens( file_data[ind:] )[0]
                present_text = file_data[ ind : ind + closing_ind+1 ]
                predicates_list.append(present_text)

        return predicates_list

data_file_path = "data/data.json"

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
    name = get_domain_name(file).strip()
    requirements = get_requirements(file)
    predicates = get_predicates(file)
    
    if name not in data.keys():
        data[name] = {}
        data[name]["requirements"] = requirements
        data[name]["predicates"] = predicates

    write_to_json(data,data_file_path)


    



    


