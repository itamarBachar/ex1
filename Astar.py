#Itamar Bachar 318781630
from ways import compute_distance
from ways.info import SPEED_RANGES


def path(node, source2, list_parents):
    if node.junction.index == source2.junction.index:
        list_parents.append(node.junction.index)
        return list_parents
    else:
        list_parents.append(node.junction.index)
    return path(node.parent, source2, list_parents)


def is_in_close(closed_list, child):
    for key in closed_list.keys():
        if child.junction.index == closed_list[key].index:
            return False
    return True


class AstarNode:
    def __init__(self, junction, parent=None, path_cost=0, hurisitc_cost=0):
        self.junction = junction
        self.parent = parent
        self.path_cost = path_cost
        self.huristic_cost = hurisitc_cost
        self.cost_all = path_cost + hurisitc_cost

    def friends(self, end, roads):
        lst = []
        for link in self.junction.links:
            target2 = roads[link.target]
            #  hurstic ditance.
            cost1 = compute_distance(target2.lat, target2.lon, end.junction.lat, end.junction.lon)
            cost1 = cost1 / 110
            # sum distance
            add = link.distance / (SPEED_RANGES[link.highway_type][1] * 1000)
            cost2 = self.path_cost + add
            lst.append(AstarNode(target2, self, cost2, cost1))
        return lst


class Queue_Astar:
    def __init__(self):
        self.lst = {}

    def add(self, node):
        for key in self.lst.keys():
            if node.junction.index == self.lst[key].junction.index:
                return
        self.lst[node.junction.index] = node

    def pop(self):
        min_path = float('inf')
        keep_node = AstarNode
        key_keep = 0
        for key in self.lst.keys():
            if min_path > self.lst[key].cost_all:
                min_path = self.lst[key].cost_all
                keep_node = self.lst[key]
                key_keep = key
        self.lst.pop(key_keep)
        return keep_node

    def get_cost(self, junc):
        for key in self.lst.keys():
            if self.lst[key].junction == junc:
                return self.lst[key].cost_all

    def delete(self, child_junc):
        key2 = 0
        for key in self.lst.keys():
            if self.lst[key].junction == child_junc:
                key2 = key
                break
        self.lst.pop(key2)

    def is_in(self, junction):
        for keys in self.lst.keys():
            if self.lst[keys].junction == junction:
                return True
        return False


def find_astar_route_help(source, target, roads):
    node_source = AstarNode(roads[source])
    node_target = AstarNode(roads[target])
    dev = 110
    ret_cost_hest = compute_distance(node_source.junction.lat, node_source.junction.lon, node_target.junction.lat,
                                     node_target.junction.lon) / dev
    frontier = Queue_Astar()  # Priority Queue
    frontier.add(node_source)
    closed_list = {}
    index = 0
    while frontier:
        node = frontier.pop()
        if node.junction == node_target.junction:
            log = path(node, node_source, [])
            return log[::-1], node.path_cost, ret_cost_hest
        closed_list[index] = node.junction
        lst_friends = node.friends(node_target, roads)
        for child in lst_friends:
            if is_in_close(closed_list, child) and not frontier.is_in(child.junction):
                frontier.add(child)
            elif frontier.is_in(child.junction) and child.path_cost < frontier.get_cost(child.junction):
                frontier.delete(child.junction)
                frontier.add(child)
        index += 1
    return None
