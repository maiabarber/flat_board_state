from search_node import search_node
from flat_board_state import flat_board_state
import heapq

count_generated = 0
count_expanded = 0

def create_open_set():
    """
    Creates and returns an empty open set.
    The open set is a priority queue of search nodes (f, id(vn), vn).
    :return: An empty priority queue representing the open set.
    """
    return []


def create_closed_set():
    """
    Creates and returns an empty closed set.
    The closed set is a dictionary that keeps track of explored states.
    :return: An empty dictionary representing the closed set.
    """
    return {}

def add_to_open(vn, open_set):
    """
    Adds a node to the open set.
    :param vn: The search node to add.
    :param open_set: The open set to which the node will be added.
    """
    heapq.heappush(open_set, (vn.f, id(vn), vn))


def open_not_empty(open_set):
    """
    Checks if the open set is not empty.
    :param open_set: The open set to check.
    :return: True if the open set is not empty, False otherwise.
    """
    return len(open_set) > 0


def get_best(open_set):
    """
    Gets the node with the lowest f-value from the open set.
    :param open_set: The open set from which to get the best node.
    :return: The search node with the lowest f-value.
    """
    return heapq.heappop(open_set)[2]


def add_to_closed(vn, closed_set):
    """
    Adds an explored node to the closed set.
    :param vn: The search node to add.
    :param closed_set: The closed set to which the node will be added.
    """
    closed_set[vn.state] = vn

#returns False if curr_neighbor state not in open_set or has a lower g from the node in open_set
#remove the node with the higher g from open_set (if exists)
def duplicate_in_open(vn, open_set):
    """
    Checks if the state already exists in the open set.
    Keeps the node with the lower g value.
    :param vn: The search node to check.
    :param open_set: The open set to check against.
    :return: True if an equal or better node already exists,
             False otherwise.
    """
    for entry in open_set:
        node = entry[2]

        if node.state == vn.state:
            if node.g <= vn.g:
                return True

            open_set.remove(entry)
            heapq.heapify(open_set)
            return False

    return False

#returns False if curr_neighbor state not in closed_set or has a lower g from the node in closed_set
#remove the node with the higher g from closed_set (if exists)
def duplicate_in_closed(vn, closed_set):
    """
    Checks if the state already exists in the closed set.
    Removes the existing node if the new path has a lower g.
    :param vn: The search node to check.
    :param closed_set: The closed set to check against.
    :return: True if an equal or better node already exists,
             False otherwise.
    """
    if vn.state in closed_set:
        node = closed_set[vn.state]

        if node.g <= vn.g:
            return True

        del closed_set[vn.state]

    return False


# helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)

def get_gen_exp_count():
    global count_generated
    global count_expanded
    return count_generated, count_expanded

def search(start_state, heuristic):
    global count_generated
    global count_expanded
    count_generated = 0
    count_expanded = 0
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)

        if flat_board_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)
        count_expanded += 1

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_closed(curr_neighbor, closed_set) and not duplicate_in_open(curr_neighbor, open_set):
                add_to_open(curr_neighbor, open_set)
                count_generated += 1

    return None




