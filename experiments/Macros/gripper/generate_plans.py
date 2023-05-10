import os
import subprocess
import glob
import random

problem_files = glob.glob("problem_files/*.pddl")
selected_files = random.sample(problem_files, 20)

output_folder = "plans"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

domain_file1 = "domain.pddl"
domain_file2 = "domain_test.pddl"
planner_path = "/Users/bittu/Desktop/GitHub/downward/"

for file in selected_files:
    print("Generating Plan for Problem: " + file, end="\r")

    output_file_path = os.path.join(output_folder, os.path.basename(file).replace("problem", "test_plan").replace(".pddl", ".txt"))
    log_output = os.path.join(output_folder, os.path.basename(file).replace("problem", "test_log").replace(".pddl", ".txt"))

    os.system(planner_path + "/fast-downward.py --plan-file " + output_file_path + " " + domain_file2 + " " + file + " --search \"astar(lmcut())\" > " + log_output)

    ########################################### domain without macros #################################################################

    output_file_path = os.path.join(output_folder, os.path.basename(file).replace("problem", "plan").replace(".pddl", ".txt"))
    log_output = os.path.join(output_folder, os.path.basename(file).replace("problem", "log").replace(".pddl", ".txt"))

    os.system(planner_path + "/fast-downward.py --plan-file " + output_file_path + " " + domain_file1 + " " + file + " --search \"astar(lmcut())\" > " + log_output)
