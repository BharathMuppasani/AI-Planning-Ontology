from ast import unaryop
from enum import unique
from lib2to3.pgen2 import driver
import random
import sys
import json
import os

def write_to_pddl( problem_name, objects, init_state, goal_state ):
    # print(problem_name)
    with open('problem_template.pddl', 'r') as f:
        lines = f.readlines()
        for l in range(len(lines)):
            if '(problem' in lines[l]:
                problem_line = l
            if '(:objects' in lines[l]:
                objects_line = l


    lines[problem_line] = '(define (problem '+problem_name+')\n'
    lines[objects_line] = '(:objects \n'+objects+' )\n'
    
    for i in range(len(lines)):
        if '(:init' in lines[i]:
            initial_line = i+1
    lines[initial_line] = init_state
    
    for i in range(len(lines)):
        if '(:goal' in lines[i]:
            goal_line = i+1
    lines[goal_line] = goal_state

    if os.path.exists('problems/') == False:
        os.mkdir('problems/')

    with open('problems/'+problem_name+'.pddl', 'w') as write_file:
        lines = "".join(lines)
        write_file.write(lines)
    write_file.close()


def generate_init_goal_states(init, goal, driver_list, truck_list, location_graph_list, locations, packages):
    
    init_list = [int(i) for i in init.split(' ')]
    goal_list = [int(i) for i in goal.split(' ')]
    
    driver_list_str = ['driver' + str(i+1) for i in range(len(driver_list))]
    truck_list_str = ['truck' + str(i+1) for i in range(len(truck_list))]
    package_list_str = ['package' + str(i+1) for i in range(packages)]
    location_list_str = ['s' + str(i+1) for i in range(locations)]
    
    objects = ' '.join(driver_list_str) + ' - driver \n' + ' '.join(truck_list_str) + ' - truck \n' + ' '.join(package_list_str) + ' - obj \n' + ' '.join(location_list_str) + ' - location \n'
    
    init_items = []
    
    for i in range(len(driver_list)):
        init_items.append(f'(at driver{str(i+1)} s{str(driver_list[i])})')
    
    for i in range(len(truck_list)):
        init_items.append(f'(at truck{str(i+1)} s{str(truck_list[i])})')
        init_items.append(f'(empty truck{str(i+1)})')
    
    unique_pair_set = set(list())
    for key, value in location_graph_list.items():
        
        for vtx in value:
            if f"{key} {vtx}" not in unique_pair_set:
                if f"{vtx} {key}" not in unique_pair_set:
                    unique_pair_set.add(f"{key} {vtx}")
                    unique_pair_set.add(f"{vtx} {key}")
                
                if (key in truck_list) and (vtx in truck_list):
                    path_or_link = 'link'
                elif (key in init_list) and (vtx in goal_list):
                    path_or_link = 'link'
                elif (key in goal_list) and (vtx in init_list):
                    path_or_link = 'link'
                else:
                    path_or_link = random.choice(['path', 'link'])
            
                if path_or_link == 'path':
                    init_items.append(f'(path {location_list_str[key-1]} {location_list_str[vtx-1]})')
                    init_items.append(f'(path {location_list_str[vtx-1]} {location_list_str[key-1]})')
                else:
                    init_items.append(f'(link {location_list_str[key-1]} {location_list_str[vtx-1]})')
                    init_items.append(f'(link {location_list_str[vtx-1]} {location_list_str[key-1]})')
    
    for i in range(len(init_list)):
        init_items.append(f'(at package{str(i+1)} s{str(init_list[i])})')
    
    goal_items = []
    
    for i in range(len(goal_list)):
        goal_items.append(f'(at package{str(i+1)} s{str(goal_list[i])})')

    
    return objects, '\n'.join(init_items), '\n'.join(goal_items)


def generate_state_combinations( list_of_states, drivers, trucks, packages, locations ):
    print(f'Generating Problem Files for {drivers} drivers, {trucks} trucks, {packages} packages, {locations} locations ', end = ' ')
    name = f'problem_{drivers}_{trucks}_{packages}_{locations}'
    counter = 0

    flag = 0
    for i in list_of_states:
        for j in list_of_states:
            if i != j:
                driver_list = [random.choice(location_list) for i in range(number_of_drivers)]
                truck_list = [random.choice(location_list) for i in range(number_of_trucks)]
                location_graph_dict = { i+1 : sorted(random.sample([unq for unq in location_list if unq != i+1], random.randint(1, number_of_locations-1))) for i in range(number_of_locations) }
                # print(location_graph_dict)
                counter += 1
                objects, init_string, goal_string = generate_init_goal_states(i,j, driver_list, truck_list, location_graph_dict, locations, packages)
                write_to_pddl(name+str(counter), objects, init_string, goal_string)
                
                if counter == 5000:
                    flag = 1
            
            if flag == 1:
                break
        
        if flag == 1:
            break
                

    print('problem file count = ', counter)

if __name__ == "__main__":

    number_of_drivers = int(sys.argv[1])
    number_of_trucks = int(sys.argv[2])
    number_of_packages = int(sys.argv[3])
    number_of_locations = int(sys.argv[4])
    
    location_list = [i+1 for i in range(number_of_locations)]
    
    states_dict_list = []
    unique_set = set(list())
    for i in range(10000):
        packages_list = [random.choice(location_list) for i in range(number_of_packages)]
        packages_str = ' '.join(str(package) for package in packages_list)
        
        if packages_str not in unique_set:
            unique_set.add(packages_str)
            states_dict_list.append(packages_str)

    generate_state_combinations(states_dict_list, number_of_drivers, number_of_trucks, number_of_packages, number_of_locations)
    
    