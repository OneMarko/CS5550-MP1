from test_grids import EXAMPLE, parse_grid
from vacuum_world import VacuumWorld

grid, start, dirty = parse_grid(EXAMPLE)
problem = VacuumWorld(grid, start, dirty)
print(problem.render())

s0 = problem.initial_state()
original_pos, original_dirty = s0[0], set(s0[1])


def unchanged(state):
    """Return True if state still matches the initial position and dirt."""
    return state[0] == original_pos and set(state[1]) == original_dirty


# state types
assert isinstance(s0, tuple) and isinstance(s0[0], tuple), type(s0)
assert isinstance(s0[1], frozenset), type(s0[1])
assert original_pos == (0, 0)
assert original_dirty == {(0, 2), (1, 3), (2, 0), (3, 2)}, original_dirty

# a move changes the position only
s1 = problem.result(s0, 'MOVE_DOWN')
assert s1 == ((1, 0), s0[1]), s1
assert unchanged(s0), s0

# walk to (0, 2) and clean it
s = problem.result(problem.result(s0, 'MOVE_RIGHT'), 'MOVE_RIGHT')
assert s[0] == (0, 2), s
assert problem.get_actions(s) == ['MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT', 'CLEAN'], problem.get_actions(s)
s_clean = problem.result(s, 'CLEAN')
assert s_clean[0] == (0, 2), s_clean
assert set(s_clean[1]) == original_dirty - {(0, 2)}, s_clean[1]
assert set(s[1]) == original_dirty, "state before CLEAN was mutated"
assert unchanged(s0), s0

# robot on dirt renders as *, robot alone as R
assert problem.render(s).splitlines()[0] == "..*.", problem.render(s)
assert problem.render(s0).splitlines()[0] == "R.D.", problem.render(s0)
assert problem.render(s_clean).splitlines()[0] == "..R.", problem.render(s_clean)

# walls, edges, and corners
assert problem.get_actions(s0) == ['MOVE_DOWN', 'MOVE_RIGHT']
assert problem.get_actions(((1, 0), s0[1])) == ['MOVE_UP', 'MOVE_DOWN']
assert problem.get_actions(((2, 2), s0[1])) == ['MOVE_UP', 'MOVE_DOWN', 'MOVE_RIGHT']
assert problem.get_actions(((3, 3), s0[1])) == ['MOVE_UP', 'MOVE_LEFT']
assert problem.get_actions(((2, 0), s0[1])) == ['MOVE_UP', 'MOVE_DOWN', 'CLEAN']

# goal test and cost
assert problem.is_goal(s0) is False
assert problem.is_goal(((0, 0), frozenset())) is True
assert problem.action_cost(s0, 'MOVE_DOWN') == 1
assert problem.action_cost(s, 'CLEAN') == 1

# states are hashable and distinct
assert len({s0, s1, s, s_clean}) == 4

print("all Part 1 checks passed")