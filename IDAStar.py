#Itamar Bachar 318781630
from ways import compute_distance
from ways.info import SPEED_RANGES

new_limit = 0


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


def path(node_source, lst):
    while node_source.parent:
        lst.append(node_source.junction.index)
        if node_source.parent is not None:
            node_source = node_source.parent
    lst.append(node_source.junction.index)
    return lst


def dfs(node_source, node_target, f_limit, roads):
    global new_limit
    new_f = node_source.cost_all
    if new_f > f_limit:
        new_limit = min(new_f, new_limit)
        return None, None
    if node_source.junction == node_target.junction:
        return path(node_source, []), node_source.cost_all
    lst_friends = node_source.friends(node_target, roads)
    for child in lst_friends:
        sol, cost = dfs(child, node_target, f_limit, roads)
        if sol:
            return sol, cost
    return None, None


def find_idastar_route_help(source, target, roads):
    global new_limit
    dev = 110
    new_limit = compute_distance(roads[source].lat, roads[source].lon, roads[target].lat,
                                 roads[target].lon) / dev
    node_source = AstarNode(roads[source], None, 0, new_limit)
    node_target = AstarNode(roads[target])
    while True:
        f_limit = new_limit
        new_limit = float('inf')
        sol = dfs(node_source, node_target, f_limit, roads)
        if sol != (None , None):
            solution , cost = sol
            solution.reverse()
            return solution , cost
