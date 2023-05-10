import os
import subprocess
import glob
import random
import shutil
import pandas as pd
import json
import random

def extract_params(output_file):
    with open(output_file, 'r') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    expanded = 0
    evaluated = 0
    generated = 0
    search_time = 300 
    total_time = 300
    plan_cost = 0
    for line in lines:
        if 'Expanded' in line and 'until' not in line:
            expanded = int(line.split('Expanded')[-1].strip().split(" ")[0].strip())
        elif 'Evaluated' in line and 'until' not in line:
            evaluated = int(line.split('Evaluated')[-1].strip().split(" ")[0].strip())
        elif 'Generated' in line and 'until' not in line:
            generated = int(line.split('Generated')[-1].strip().split(" ")[0].strip())
        elif 'Search time' in line:
            search_time = round(float(line.split(':')[-1].strip().replace('s', '')), 6)
        elif 'Total time' in line:
            total_time = round(float(line.split(':')[-1].strip().replace('s', '')), 6)
        elif 'Plan cost:' in line:
            plan_cost = int(line.split(':')[-1].strip())

    return expanded, evaluated, generated, search_time, total_time, plan_cost

random.seed(123)
current_path = os.getcwd()

planner_path = "/home/bharath/Desktop/GitHub/downward"
domains= [f for f in glob.glob(current_path + "/data/*") if os.path.isdir(f)]

prefix_config = 'seq-opt-'
planner_configs = ['fdss-1', 'bjolp', 'lmcut', 'merge-and-shrink']
planner_results = pd.read_csv('ipc2011_results.csv')


best_config = {}
for domain in domains:
    if os.path.basename(domain) in planner_results.columns:
        fdss_score = planner_results[os.path.basename(domain)][ planner_results['planner'] == 'fdss-1' ].values[0]
        bjolp_score = planner_results[os.path.basename(domain)][ planner_results['planner'] == 'bjolp' ].values[0]
        lmcut_score = planner_results[os.path.basename(domain)][ planner_results['planner'] == 'lmcut' ].values[0]
        merge_and_shrink_score = planner_results[os.path.basename(domain)][ planner_results['planner'] == 'merge-and-shrink' ].values[0]
        
        # Determine the best planner configuration
        best_score = max(fdss_score, bjolp_score, lmcut_score)
        if best_score == lmcut_score:
            best_planner = 'lmcut'
        elif best_score == fdss_score:
            best_planner = 'fdss-1'
        elif best_score == bjolp_score:
            best_planner = 'bjolp'
        elif best_score == merge_and_shrink_score:
            best_planner = 'merge-and-shrink'
        

        # Store the best planner configuration as a string in the best_config dictionary
        if os.path.basename(domain) not in best_config:
            best_config[os.path.basename(domain)] = prefix_config + best_planner

# print(json.dumps(best_config, indent=4))
#################### Random Selection ##############################

print("Running Random Selection")

if not os.path.exists( os.path.join(current_path, 'random_policy_results') ):
    os.makedirs( os.path.join(current_path, 'random_policy_results') )

main_log_file = os.path.join(current_path, 'random_policy_results', "randomPolicy_results_log.txt" )
main_log_content = ""
main_log_content += "###### Random Policy Results ######\n\n"

domain_list = []
random_avg_expanded = []
random_avg_evaluated = []
random_avg_generated = []
random_avg_total_time = []
random_avg_plan_cost = []

for domain in domains:
    print(os.path.basename(domain))
    main_log_content += f"------------------{os.path.basename(domain)}----------------------\n\n"

    domain_file = os.path.join(domain, 'domain.pddl')
    problem_files = glob.glob(domain + '/instance*.pddl')

    avg_expanded = 0
    avg_evaluated = 0
    avg_generated = 0
    avg_total_time = 0
    avg_plan_cost = 0

    domain_list.append(os.path.basename(domain))
    if os.path.exists(domain_file):
        for problem_file in problem_files:

            choice = random.choice(planner_configs)
            selected_config = prefix_config + choice

            main_log_content += f"Domain: {os.path.basename(domain)}\n"
            main_log_content += f"Problem: {os.path.basename(problem_file)}\n"
            main_log_content += f"Selected Config: {selected_config}\n\n"

            if not os.path.exists(os.path.join(current_path, 'random_policy_results', "results")):
                os.makedirs(os.path.join(current_path, 'random_policy_results', "results"))

            plan_file_path = os.path.join(current_path, 'random_policy_results', "results", "plan-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.txt') )
            log_output = os.path.join(current_path, 'random_policy_results', "results", "log-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.log') )

            os.system(f"{planner_path}/fast-downward.py --plan-file {plan_file_path} --alias {selected_config} --overall-time-limit 5m {domain_file} {problem_file} > {log_output}")

            expanded, evaluated, generated, search_time, total_time, plan_cost = extract_params(log_output)
            main_log_content += f"Expanded States: {expanded}\n"
            main_log_content += f"Evaluated States: {evaluated}\n"
            main_log_content += f"Generated States: {generated}\n"
            main_log_content += f"Search Time: {search_time}\n"
            main_log_content += f"Total Time: {total_time}\n"
            main_log_content += f"Plan Cost: {plan_cost}\n\n"
            main_log_content += "----------------------------------------\n\n"

            avg_expanded += expanded 
            avg_evaluated += evaluated
            avg_generated += generated
            avg_total_time += total_time
            avg_plan_cost += plan_cost
        avg_expanded = avg_expanded / len(problem_files)
        avg_evaluated = avg_evaluated / len(problem_files)
        avg_generated = avg_generated / len(problem_files)
        avg_total_time = avg_total_time / len(problem_files)
        avg_plan_cost = avg_plan_cost / len(problem_files)

        random_avg_expanded.append(avg_expanded)
        random_avg_evaluated.append(avg_evaluated)
        random_avg_generated.append(avg_generated)
        random_avg_total_time.append(avg_total_time)
        random_avg_plan_cost.append(avg_plan_cost)

        main_log_content += "-------------- Averages --------------\n"
        main_log_content += f"Average Expanded States: {avg_expanded}\n"
        main_log_content += f"Average Evaluated States: {avg_evaluated}\n"
        main_log_content += f"Average Generated States: {avg_generated}\n"
        main_log_content += f"Average Total Time: {avg_total_time}\n"
        main_log_content += f"Average Plan Cost: {avg_plan_cost}\n\n"
        main_log_content += "----------------------------------------\n\n"
    else:
        for problem_file in problem_files:

            choice = random.choice(planner_configs)
            selected_config = prefix_config + choice


            domain_file = os.path.join(domain, os.path.basename(problem_file).replace('instance', 'domain'))
            main_log_content += f"Domain: {os.path.basename(domain)}\n"
            main_log_content += f"Problem: {os.path.basename(problem_file)}\n"
            main_log_content += f"Selected Config: {selected_config}\n\n"

            if not os.path.exists(os.path.join(current_path, 'random_policy_results', "results")):
                os.makedirs(os.path.join(current_path, 'random_policy_results', "results"))

            plan_file_path = os.path.join(current_path, 'random_policy_results', "results", "plan-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.txt') )
            log_output = os.path.join(current_path, 'random_policy_results', "results", "log-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.log') )

            os.system(f"{planner_path}/fast-downward.py --plan-file {plan_file_path} --alias {selected_config} --overall-time-limit 5m {domain_file} {problem_file} > {log_output}")

            expanded, evaluated, generated, search_time, total_time, plan_cost = extract_params(log_output)
            main_log_content += f"Expanded States: {expanded}\n"
            main_log_content += f"Evaluated States: {evaluated}\n"
            main_log_content += f"Generated States: {generated}\n"
            main_log_content += f"Search Time: {search_time}\n"
            main_log_content += f"Total Time: {total_time}\n"
            main_log_content += f"Plan Cost: {plan_cost}\n\n"
            main_log_content += "----------------------------------------\n\n"

            avg_expanded += expanded 
            avg_evaluated += evaluated
            avg_generated += generated
            avg_total_time += total_time
            avg_plan_cost += plan_cost
        avg_expanded = avg_expanded / len(problem_files)
        avg_evaluated = avg_evaluated / len(problem_files)
        avg_generated = avg_generated / len(problem_files)
        avg_total_time = avg_total_time / len(problem_files)
        avg_plan_cost = avg_plan_cost / len(problem_files)

        random_avg_expanded.append(avg_expanded)
        random_avg_evaluated.append(avg_evaluated)
        random_avg_generated.append(avg_generated)
        random_avg_total_time.append(avg_total_time)
        random_avg_plan_cost.append(avg_plan_cost)

        main_log_content += "-------------- Averages --------------\n"
        main_log_content += f"Average Expanded States: {avg_expanded}\n"
        main_log_content += f"Average Evaluated States: {avg_evaluated}\n"
        main_log_content += f"Average Generated States: {avg_generated}\n"
        main_log_content += f"Average Total Time: {avg_total_time}\n"
        main_log_content += f"Average Plan Cost: {avg_plan_cost}\n\n"
        main_log_content += "----------------------------------------\n\n"

with open(main_log_file, 'w') as f:
    f.write(main_log_content)

###################### Ontology Config Selection ############################

print("Running Ontology Config Selection")

if not os.path.exists( os.path.join(current_path, 'ontology_policy_results') ):
    os.makedirs( os.path.join(current_path, 'ontology_policy_results') )

main_log_file = os.path.join(current_path, 'ontology_policy_results', "ontologyPolicy_results_log.txt" )
main_log_content = ""
main_log_content += "###### Best Policy Results ######\n"

ontology_avg_expanded = []
ontology_avg_evaluated = []
ontology_avg_generated = []
ontology_avg_total_time = []
ontology_avg_plan_cost = []

for domain in domains:
    print(os.path.basename(domain))
    main_log_content += f"------------------{os.path.basename(domain)}----------------------\n\n"

    selected_config = best_config[os.path.basename(domain)]

    domain_file = os.path.join(domain, 'domain.pddl')
    problem_files = glob.glob(domain + '/instance*.pddl')

    avg_expanded = 0
    avg_evaluated = 0
    avg_generated = 0
    avg_total_time = 0
    avg_plan_cost = 0

    if os.path.exists(domain_file):
        for problem_file in problem_files:
            main_log_content += f"Domain: {os.path.basename(domain)}\n"
            main_log_content += f"Problem: {os.path.basename(problem_file)}\n"
            main_log_content += f"Selected Config: {selected_config}\n\n"

            if not os.path.exists(os.path.join(current_path, 'ontology_policy_results', "results")):
                os.makedirs(os.path.join(current_path, 'ontology_policy_results', "results"))

            plan_file_path = os.path.join(current_path, 'ontology_policy_results', "results", "plan-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.txt') )
            log_output = os.path.join(current_path, 'ontology_policy_results', "results", "log-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.log') )

            os.system(f"{planner_path}/fast-downward.py --plan-file {plan_file_path} --alias {selected_config} --overall-time-limit 5m {domain_file} {problem_file} > {log_output}")

            expanded, evaluated, generated, search_time, total_time, plan_cost = extract_params(log_output)
            main_log_content += f"Expanded States: {expanded}\n"
            main_log_content += f"Evaluated States: {evaluated}\n"
            main_log_content += f"Generated States: {generated}\n"
            main_log_content += f"Search Time: {search_time}\n"
            main_log_content += f"Total Time: {total_time}\n"
            main_log_content += f"Plan Cost: {plan_cost}\n\n"
            main_log_content += "----------------------------------------\n\n"

            avg_expanded += expanded 
            avg_evaluated += evaluated
            avg_generated += generated
            avg_total_time += total_time
            avg_plan_cost += plan_cost
        avg_expanded = avg_expanded / len(problem_files)
        avg_evaluated = avg_evaluated / len(problem_files)
        avg_generated = avg_generated / len(problem_files)
        avg_total_time = avg_total_time / len(problem_files)
        avg_plan_cost = avg_plan_cost / len(problem_files)

        ontology_avg_expanded.append(avg_expanded)
        ontology_avg_evaluated.append(avg_evaluated)
        ontology_avg_generated.append(avg_generated)
        ontology_avg_total_time.append(avg_total_time)
        ontology_avg_plan_cost.append(avg_plan_cost)

        main_log_content += "-------------- Averages --------------\n"
        main_log_content += f"Average Expanded States: {avg_expanded}\n"
        main_log_content += f"Average Evaluated States: {avg_evaluated}\n"
        main_log_content += f"Average Generated States: {avg_generated}\n"
        main_log_content += f"Average Total Time: {avg_total_time}\n"
        main_log_content += f"Average Plan Cost: {avg_plan_cost}\n\n"
        main_log_content += "----------------------------------------\n\n"

    else:
        for problem_file in problem_files:
            domain_file = os.path.join(domain, os.path.basename(problem_file).replace('instance', 'domain'))
            main_log_content += f"Domain: {os.path.basename(domain)}\n"
            main_log_content += f"Problem: {os.path.basename(problem_file)}\n"
            main_log_content += f"Selected Config: {selected_config}\n\n"

            if not os.path.exists(os.path.join(current_path, 'ontology_policy_results', "results")):
                os.makedirs(os.path.join(current_path, 'ontology_policy_results', "results"))

            plan_file_path = os.path.join(current_path, 'ontology_policy_results', "results", "plan-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.txt') )
            log_output = os.path.join(current_path, 'ontology_policy_results', "results", "log-" + os.path.basename(domain) + '-' + os.path.basename(problem_file).replace('.pddl', '.log') )

            os.system(f"{planner_path}/fast-downward.py --plan-file {plan_file_path} --alias {selected_config} --overall-time-limit 5m {domain_file} {problem_file} > {log_output}")

            expanded, evaluated, generated, search_time, total_time, plan_cost = extract_params(log_output)
            main_log_content += f"Expanded States: {expanded}\n"
            main_log_content += f"Evaluated States: {evaluated}\n"
            main_log_content += f"Generated States: {generated}\n"
            main_log_content += f"Search Time: {search_time}\n"
            main_log_content += f"Total Time: {total_time}\n"
            main_log_content += f"Plan Cost: {plan_cost}\n\n"
            main_log_content += "----------------------------------------\n\n"

            avg_expanded += expanded 
            avg_evaluated += evaluated
            avg_generated += generated
            avg_total_time += total_time
            avg_plan_cost += plan_cost
        avg_expanded = avg_expanded / len(problem_files)
        avg_evaluated = avg_evaluated / len(problem_files)
        avg_generated = avg_generated / len(problem_files)
        avg_total_time = avg_total_time / len(problem_files)
        avg_plan_cost = avg_plan_cost / len(problem_files)

        ontology_avg_expanded.append(avg_expanded)
        ontology_avg_evaluated.append(avg_evaluated)
        ontology_avg_generated.append(avg_generated)
        ontology_avg_total_time.append(avg_total_time)
        ontology_avg_plan_cost.append(avg_plan_cost)

        main_log_content += "-------------- Averages --------------\n"
        main_log_content += f"Average Expanded States: {avg_expanded}\n"
        main_log_content += f"Average Evaluated States: {avg_evaluated}\n"
        main_log_content += f"Average Generated States: {avg_generated}\n"
        main_log_content += f"Average Total Time: {avg_total_time}\n"
        main_log_content += f"Average Plan Cost: {avg_plan_cost}\n\n"
        main_log_content += "----------------------------------------\n\n"

with open(main_log_file, 'w') as f:
    f.write(main_log_content)


df = pd.DataFrame()
df['Domains'] = domains
df['Ont Avg Expanded'] = ontology_avg_expanded
df['Ont Avg Evaluated'] = ontology_avg_evaluated
df['Ont Avg Generated'] = ontology_avg_generated
df['Ont Avg Total Time'] = ontology_avg_total_time
df['Ont Avg Plan Cost'] = ontology_avg_plan_cost

df['Random Avg Expanded'] = random_avg_expanded
df['Random Avg Evaluated'] = random_avg_evaluated
df['Random Avg Generated'] = random_avg_generated
df['Random Avg Total Time'] = random_avg_total_time
df['Random Avg Plan Cost'] = random_avg_plan_cost

df.to_csv('results.csv', index=False)
# ################# COPY IPC-2011 data to Data folder #####################

# current_path = os.getcwd()
# domains_path = "/Users/bittu/Desktop/GitHub/pddl-instances/ipc-2011/domains/"
# domains = [f for f in glob.glob(domains_path + "*") if 'sequential-optimal' in f]
# # print('\n'.join(domains))

# if not os.path.exists( os.path.join(current_path, 'data') ):
#     os.makedirs( os.path.join(current_path, 'data') )

# for domain in domains:
#     domain_file = os.path.join(domain, 'domain.pddl')
#     domain_name = os.path.basename(domain).replace('-sequential-optimal', '')

#     if not os.path.exists( os.path.join(current_path, 'data', domain_name) ):
#         os.makedirs( os.path.join(current_path, 'data', domain_name) )

#     if not os.path.exists(domain_file):
#         for i in range(1,4):
#             domain_file = os.path.join(domain, 'domains' , 'domain-' + str(i) + '.pddl')
#             if os.path.exists(domain_file):
#                 shutil.copy(domain_file, os.path.join(current_path, 'data', domain_name, 'domain-'+str(i)+'.pddl'))
#     else:
#         shutil.copy(domain_file, os.path.join(current_path, 'data',domain_name, 'domain.pddl'))

#     problem_path = domain + '/instances/'
#     for i in range(1,4):
#         shutil.copy(problem_path + 'instance-'+str(i)+'.pddl', os.path.join(current_path, 'data', domain_name, 'instance-'+str(i)+'.pddl'))