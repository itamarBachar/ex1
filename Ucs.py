#Itamar Bachar 318781630
from ways.info import SPEED_RANGES


class Node:
    def __init__(self, junction, parent=None, path_cost=0):
        self.junction = junction
        self.parent = parent
        self.path_cost = path_cost

    def friends(self, roads):
        lst = []
        for link in self.junction.links:
            target2 = roads[link.target]
            add = link.distance / (SPEED_RANGES[link.highway_type][1] * 1000)
            cost2 = self.path_cost + add
            lst.append(Node(target2, self, cost2))
        return lst


class Queue:
    def __init__(self):
        self.lst = {}

    def add(self, node):
        for key in self.lst.keys():
            if node.junction.index == self.lst[key].junction.index:
                return
        self.lst[node.junction.index] = node

    def pop(self):
        min_path = float('inf')
        keep_node = Node
        key_keep = 0
        for key in self.lst.keys():
            if min_path > self.lst[key].path_cost:
                min_path = self.lst[key].path_cost
                keep_node = self.lst[key]
                key_keep = key
        self.lst.pop(key_keep)
        return keep_node

    def get_cost(self, junc):
        for key in self.lst.keys():
            if self.lst[key].junction == junc:
                return self.lst[key].path_cost

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


# return the path.

def path(node, source2, list_parents):
    if node.junction.index == source2.junction.index:
        list_parents.append(node.junction.index)
        return list_parents
    else:
        list_parents.append(node.junction.index)
    return path(node.parent, source2, list_parents)


def find_ucs_rout_help(source, target, roads):
    node_source = Node(roads[source])
    node_target = Node(roads[target])
    frontier = Queue()  # Priority Queue
    frontier.add(node_source)
    closed_list = {}
    index = 0
    while frontier:
        node = frontier.pop()
        if node.junction == node_target.junction:
            log = path(node, node_source, [])
            return log[::-1], node.path_cost
        closed_list[index] = node.junction
        lst_friends = node.friends(roads)
        for child in lst_friends:
            if is_in_close(closed_list, child) and not frontier.is_in(child.junction):
                frontier.add(child)
            elif frontier.is_in(child.junction) and child.path_cost < frontier.get_cost(child.junction):
                frontier.delete(child.junction)
                frontier.add(child)
        index += 1
    return None


def is_in_close(closed_list, child):
    for key in closed_list.keys():
        if child.junction.index == closed_list[key].index:
            return False
    return True
