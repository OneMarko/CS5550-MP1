"""
CS3810 Mini-Project 1 - Part 2: The Search Algorithms (100 points)
==================================================================

Implement dfs_search, astar_search, and idastar_search below. Do not change
the signatures or the return shapes: run_tests.py and the grading harness
unpack them exactly as documented.

You may NOT use a library implementation of DFS, A*, or IDA* (networkx,
simpleai, aima-python, ...). Using heapq, collections.deque, and the
provided PriorityQueue is expected and fine.

Metric definitions - use these, and say which you used in your report:

    nodes_expanded      A node is EXPANDED when it is removed from the
                        frontier and its successors are generated. Do not
                        count nodes that were merely generated.

    max_frontier_size   The largest number of live entries the frontier
                        ever held. For the PriorityQueue helper this is
                        len(queue), not len(queue.heap).

    iterations          (IDA* only) The number of depth-limited passes,
                        i.e. how many times the f-cost threshold was set.
                        A search that succeeds on the first threshold has
                        iterations == 1.

Suggested order of work: DFS first, then A*, then IDA*.
"""

import math

from priority_queue import PriorityQueue

# Sentinel used by the IDA* recursion to report success. Returning a plain
# number means "the smallest f-value I saw above the threshold".
FOUND = 'FOUND'


def dfs_search(problem):
    """
    Perform Depth-First Search.

    Args:
        problem: VacuumWorld instance

    Returns:
        Tuple (solution_path, nodes_expanded, max_frontier_size)
        solution_path: List of actions, or None if no solution
        nodes_expanded: Number of nodes expanded during search
        max_frontier_size: Maximum size of frontier during search

    Requirements:
        * Iterative, with an explicit stack. Do NOT recurse - you will hit
          Python's recursion limit on the larger grids.
        * Cycle detection with an explored set, or DFS will not terminate.
        * Returns the FIRST solution found. It will not be optimal, and it
          is not supposed to be.

    Hint: push (state, path_so_far) pairs. Push successors in reversed()
    order if you want the stack to explore them in ACTION_ORDER order.
    """
    
    # stack of state and path_so_far
    stack = [(problem.initial_state(), [])]
    explored = set()
    nodes_expanded = 0
    max_frontier_size = 1
    
    while stack :
        state, path_so_far = stack.pop()
        if problem.is_goal(state):
            return path_so_far, nodes_expanded, max_frontier_size
        
        if state not in explored:
            explored.add(state)
            nodes_expanded += 1
            
            for action in reversed(problem.get_actions(state)):
                next_state = problem.result(state, action)
                stack.append((next_state, path_so_far + [action]))
        
        max_frontier_size = max(max_frontier_size, len(stack))
    
    return None, nodes_expanded, max_frontier_size




def astar_search(problem, heuristic):
    """
    Perform A* Search.

    Args:
        problem: VacuumWorld instance
        heuristic: Function h(state, problem) -> estimated cost to goal

    Returns:
        Tuple (solution_path, nodes_expanded, max_frontier_size)

    Requirements:
        * Priority queue ordered by f(n) = g(n) + h(n).
        * Handle REOPENING: if you find a cheaper path to a state you have
          already expanded, you must be able to improve it. The provided
          PriorityQueue supports this - pushing an item already in the
          queue replaces its priority instead of duplicating it.
        * With an admissible heuristic this MUST return an optimal
          solution. run_tests.py checks that against known optimal costs.

    Hint: keep a dict g[state] of best-known cost-so-far and a dict
    came_from[state] = (parent_state, action) to rebuild the path at the
    end. A helper like _reconstruct() below keeps the main loop readable.
    """
    start = problem.initial_state()
    frontier = PriorityQueue()
    frontier.push(start, heuristic(start, problem))
    came_from = {start: (None, None)}
    g = {start: 0}
    nodes_expanded = 0
    max_frontier_size = 1
    
    while frontier:
        current = frontier.pop()
        
        if problem.is_goal(current):
            return _reconstruct(came_from, current), nodes_expanded, max_frontier_size
        
        nodes_expanded += 1
        
        for action in problem.get_actions(current):
            next_state = problem.result(current, action)
            tentative_g = g[current] + problem.action_cost(current, action)
            
            if next_state not in g or tentative_g < g[next_state]:
                g[next_state] = tentative_g
                f_value = tentative_g + heuristic(next_state, problem)
                frontier.push(next_state, f_value)
                came_from[next_state] = (current, action)
        
        max_frontier_size = max(max_frontier_size, len(frontier))
        
    return None, nodes_expanded, max_frontier_size
    

def _reconstruct(came_from, state):
    """Walk came_from backwards from `state` and return the action list.

    Args:
        came_from: Dict mapping state -> (parent_state, action)
        state: The goal state reached by the search

    Returns:
        List of actions from the initial state to `state`.
    """
    actions = []
    while state in came_from and came_from[state][0] is not None:
        state, action = came_from[state]
        actions.append(action)
    return list(reversed(actions))


def idastar_search(problem, heuristic):
    """
    Perform Iterative Deepening A* Search.

    Args:
        problem: VacuumWorld instance
        heuristic: Function h(state, problem) -> estimated cost to goal

    Returns:
        Tuple (solution_path, nodes_expanded, iterations)
        iterations: Number of depth-limited iterations performed

    Requirements:
        * Iterative deepening on an f-cost THRESHOLD, not on depth. The
          next threshold is the smallest f-value that exceeded the current
          one.
        * Linear space: no explored set carried across iterations. You may
          track the states on the current path to avoid immediate cycles.
        * Returns an optimal solution.

    Structure that works (write DFS and A* first - this will make far more
    sense once you have both):

        threshold = h(start)
        loop:
            result = search(start, g=0, threshold)
            if result is FOUND:    return the path
            if result is infinite: return None (no solution)
            threshold = result

    where search(state, g, threshold) returns FOUND, or the smallest
    f-value it saw that exceeded the threshold, or math.inf.
    """
    start = problem.initial_state()
    threshold = heuristic(start, problem)
    nodes_expanded = 0
    iterations = 0
    
    solution = None
    
    def search(state, g, threshold, path, actions):
        nonlocal nodes_expanded, solution
        f_value = g + heuristic(state, problem)
        
        if f_value > threshold:
            return f_value
        
        if problem.is_goal(state):
            solution = actions
            return FOUND
        
        nodes_expanded += 1
        min_threshold = math.inf
        
        for action in problem.get_actions(state):
            next_state = problem.result(state, action)
            if next_state not in path:  # Avoid cycles
                result = search(next_state, g + problem.action_cost(state, action), threshold, path | {next_state}, actions + [action])
                if result == FOUND:
                    return FOUND
                min_threshold = min(min_threshold, result)
        
        return min_threshold
    while True:
        iterations += 1
        result = search(start, 0, threshold, {start}, [])
        if result == FOUND:
            return solution, nodes_expanded, iterations
        if result == math.inf:
            return None, nodes_expanded, iterations
        threshold = result


if __name__ == "__main__":
    # Quick manual check once you have implemented an algorithm:
    from test_grids import EXAMPLE, parse_grid
    from vacuum_world import VacuumWorld
    from heuristics import h2

    grid, start, dirty = parse_grid(EXAMPLE)
    problem = VacuumWorld(grid, start, dirty)

    path, expanded, frontier = astar_search(problem, h2)
    print("A* on the example grid (optimal cost is 14)")
    print("  cost     :", len(path) if path else None)
    print("  expanded :", expanded)
    print("  frontier :", frontier)
    print("  plan     :", path)
