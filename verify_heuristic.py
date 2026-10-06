import os
from sokoban import Sokoban, DIRECTIONS, MOVE_COST, PUSH_COST

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(BASE_DIR, "maps")


def get_single_maps():
    if not os.path.exists(MAPS_DIR):
        return []
    return sorted(
        [f for f in os.listdir(MAPS_DIR) if f.endswith(".txt") and f != "competitive_map.txt"]
    )
def find_optimal_path_states(game):
    from collections import deque

    start = game.initial
    queue = deque([start])
    parent = {start: None}

    goal_state = None

    while queue:
        curr = queue.popleft()

        if game.is_goal(curr):
            goal_state = curr
            break

        agent, boxes = curr
        for action, direction in DIRECTIONS.items():
            dr, dc = direction
            new_agent = (agent[0] + dr, agent[1] + dc)

            if game.is_wall(new_agent):
                continue

            if new_agent in boxes:
                new_box = (new_agent[0] + dr, new_agent[1] + dc)
                if game.is_wall(new_box) or new_box in boxes:
                    continue
                new_boxes = (boxes - {new_agent}) | {new_box}
                next_state = (new_agent, new_boxes)
            else:
                next_state = (new_agent, boxes)

            if next_state not in parent:
                parent[next_state] = curr
                queue.append(next_state)

    if goal_state is None:
        return None
    path = []
    curr = goal_state
    while curr is not None:
        path.append(curr)
        curr = parent[curr]

    path.reverse()
    return path

def verify_map_path(map_path):
    print(f"--- STARTING VERIFICATION ON MAP: {map_path} ---\n")

    game = Sokoban(map_path)
    path = find_optimal_path_states(game)

    if not path:
        print("No solution found for this map!\n")
        return

    total_steps = len(path) - 1

    print("[Step-by-step details on the optimal path]")
    header = (
        f"{'Step':<5} | {'h(n)':<6} | {'h*(n)':<6} | {'h(n\')':<6} | "
        f"{'Consistent Check (h(n) <= 1 + h(n\'))':<36} | "
        f"{'Admissible Check (h(n) <= h*(n))'}"
    )
    print(header)
    print("-" * 105)

    is_all_admissible = True
    is_all_consistent = True

    for i in range(len(path)):
        curr_state = path[i]
        h_n = float(game.heuristic(curr_state))
        h_star = float(total_steps - i)

        admiss_check = h_n <= h_star
        if not admiss_check:
            is_all_admissible = False

        if i < len(path) - 1:
            next_state = path[i + 1]
            h_next = float(game.heuristic(next_state))
            cons_check = (h_n - h_next) <= 1.0 + 1e-6
            if not cons_check:
                is_all_consistent = False

            h_next_str = f"{h_next:<6.1f}"
            cons_str = f"{str(cons_check):<36}"
        else:
            h_next_str = f"{'-':<6}"
            cons_str = f"{'-':<36}"

        row = (
            f"{i:>4} | "
            f"{h_n:>5.1f} | "
            f"{int(h_star):>5} | "
            f"{h_next_str} | "
            f"{cons_str} | "
            f"{str(admiss_check)}"
        )
        print(row)

    print("-" * 105)
    print("\n[EXPERIMENTAL CONCLUSION]")
    print(f"Admissibility: {'PASSED' if is_all_admissible else 'FAILED'}")
    print(f"Consistency:   {'PASSED' if is_all_consistent else 'FAILED'}\n")

if __name__ == "__main__":
    maps = get_single_maps()
    if not maps:
        maps = ["maps/example_map.txt"] if os.path.exists("maps/example_map.txt") else ["example_map.txt"]

    for m in maps:
        target = os.path.join(MAPS_DIR, m) if os.path.exists(os.path.join(MAPS_DIR, m)) else m
        if os.path.exists(target):
            verify_map_path(target)