'''

Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''
# Itamar Bachar 318781630
# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions
import ast
import random
import time

from matplotlib import pyplot as plt

from Astar import find_astar_route_help
from IDAStar import find_idastar_route_help
from Ucs import find_ucs_rout_help
from ways import draw
from ways.tools import compute_distance
import csv
from for_help import roads


# distance from the current to the last
def huristic_function(lat1, lon1, lat2, lon2):
    return compute_distance(lat1, lon1, lat2, lon2) / 110


def find_idastar_route(source, target):
    path , cost = find_idastar_route_help(source, target, roads)
    return path


def find_ucs_rout(source, target):
    path, cost = find_ucs_rout_help(source, target, roads)
    return path


def find_astar_route(source, target):
    path, cost, cost2 = find_astar_route_help(source, target, roads)
    return path


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


def create_problems():
    map_problem = {}
    for i in range(0, 100):
        num2 = random.randint(0, 100000)
        temp = num2
        num1 = random.randint(5, 12)
        for j in range(0, num1):
            num2 = roads[num2].links[0].target
        map_problem[str(temp)] = num2
    with open('problems.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for key in map_problem:
            writer.writerow([key, map_problem[key]])


def read_problem():
    map_pro = {}
    with open('problems.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            map_pro[row[0]] = row[1]
    return map_pro


def write_result_Astar(to_return, cost, hest_cost):
    i = 0
    with open(".\\results\\AStar.txt", "w+") as f:
        for keys in to_return:
            ls = to_return[keys]
            for l in ls:
                f.write(" ")
                f.write(str(l))
            str2 = str(cost[i])
            f.write(" - ")
            f.write(str2)
            str3 = str(hest_cost[i])
            f.write(" - ")
            f.write(str3)
            f.write('\n')
            i += 1
        f.close()


def write_result(to_return, cost):
    i = 0
    with open(".\\results\\UCSRuns.txt", "w+") as f:
        for keys in to_return:
            ls = to_return[keys]
            for l in ls:
                f.write(" ")
                f.write(str(l))
            str2 = str(cost[i])
            f.write(" - ")
            f.write(str2)
            f.write('\n')
            i += 1
        f.close()


def run_ida_star_10():
    map_problem = read_problem()
    index = 0
    for key in map_problem:
        source = int(key)
        target = int(map_problem[key])
        path, cost = find_idastar_route(source, target)
        # draw.plot_path(roads, path)
        # plt.show()
        index += 1
        if index == 10:
            break


def run_ucs_100():
    map_problem = read_problem()
    to_return = {}
    cost = [0] * 100
    index = 0
    for key in map_problem:
        source = int(key)
        target = int(map_problem[key])
        to_return[key], cost[index] = find_ucs_rout(source, target)
        index += 1
    write_result(to_return, cost)


def run_astar_100():
    map_problem = read_problem()
    to_return = {}
    cost = [0] * 100
    hest_cost = [0] * 100
    index = 0
    for key in map_problem:
        source = int(key)
        target = int(map_problem[key])
        to_return[key], cost[index], hest_cost[index] = find_astar_route(source, target)
        index += 1
    write_result_Astar(to_return, cost, hest_cost)


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
