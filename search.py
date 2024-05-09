import tree_hanoi
import hanoi_states
from aima import PriorityQueue,heapq


# Definir la función heurística para la Torre de Hanoi
def hanoi_heuristic(state: hanoi_states.StatesHanoi):
    # Suponiendo que el objetivo es mover todos los discos a la tercera torre
    return len(state.rods[0]) + len(state.rods[1])

def astar_search(problem, h=None):
    """A* search algorithm."""
    h = hanoi_heuristic
    node = tree_hanoi.NodeHanoi(problem.initial)
    frontier = PriorityQueue('min', lambda n: n.path_cost + h(n.state))
    frontier.append(node)
    explored = set()

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)

        for action in problem.actions(node.state):
            child = node.child_node(problem, action)
            if child.state not in explored and all(child.state != other.state for _, other in frontier.heap):
                frontier.append(child)
            else:
                # Intentar encontrar el nodo existente y comparar path_cost
                for _, existing in frontier.heap:
                    if existing.state == child.state and existing.path_cost > child.path_cost:
                        # Reemplazar el nodo existente con el nuevo si el nuevo tiene un path_cost menor
                        frontier.heap.remove((existing.path_cost, existing))
                        frontier.heap.append((child.path_cost + h(child.state), child))
                        heapq.heapify(frontier.heap)
                        break

    return None

