#Itamar Bachar 318781630
'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
from collections import Counter

def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    lst_roads = []
    iter_for_link = roads.iterlinks()
    max_junction = 0
    min_junction = float('inf')
    max_distance = 0
    min_distance = float('inf')
    sum_distance = 0
    for junction in roads.junctions():
        max_junction = max(len(junction.links), max_junction)
        min_junction = min(len(junction.links), min_junction)
        for link in junction.links:
            lst_roads.append(link.highway_type)
            sum_distance = link.distance + sum_distance
            if link.distance > max_distance:
                max_distance = link.distance
            if link.distance < min_distance:
                min_distance = link.distance
    sum_links = 0
    for it in iter_for_link:
        sum_links = sum_links + 1
    return {
        'Number of junctions': len(roads.junctions()),
        'Number of links': sum_links,
        'Outgoing branching factor': Stat(max=max_junction, min=min_junction, avg=sum_links / len(roads.junctions()) ),
        'Link distance': Stat(max=max_distance, min=min_distance, avg=sum_distance/sum_links),
        # value should be a dictionary
        # mapping each info.road.TYPE to the no' of links of this type
        'Link type histogram' : Counter(lst_roads),  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()

