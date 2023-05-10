import os
import sys
import glob
import pandas as pd
import time
import random

def exec_com(locations, drivers, packages, trucks):
    # generate integer random number using random library
    random_number = random.randint(0, 100)
    while random_number in dic:
        random_number = random.randint(0, 100)
    
    dic[random_number] = 1
    command_str = f'./dlgen --seed {random_number} {locations} {drivers} {packages} {trucks} > problem_files/problem_{locations}_{drivers}_{packages}_{trucks}_{random_number}.pddl'
    os.system(command_str)


for locations in range(2,5):
    for drivers in range(2,5):
        for packages in range(2,4):
            for trucks in range(2,4):

                if (drivers and trucks ) > (packages and locations):
                    continue

                if (drivers < trucks - 2) or (drivers > trucks + 2):
                    continue

                dic = {}
                for seed in range(5):
                    exec_com(locations, drivers, packages, trucks)
                    print(f'{locations}, {drivers}, {packages}, {trucks}', end='\r')