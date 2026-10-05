from collections import deque
import math
import os
from sokoban import Sokoban, search



def run_heuristic_verification(game, state_limit=15000, cost_per_step=1):

    initial_state = game.initial
    all_states = set([initial_state])
    edges = {}
    reverse_edges = {}
    goal_states = set()

    queue = deque([initial_state])
    edges[initial_state] = []

    while queue:
        curr = queue.popleft()

        if game.is_goal(curr):
            goal_states.add(curr)

        if curr not in edges:
            edges[curr] = []

        for res in game.actions(curr):
            action = res[0]
            next_state = res[1]
            edges[curr].append(next_state)
            
            if next_state not in reverse_edges:
                reverse_edges[next_state] = []
            reverse_edges[next_state].append(curr)

            if next_state not in all_states:
                all_states.add(next_state)
                queue.append(next_state)

        if len(all_states) >= state_limit:
            break
    consistency_violations = 0
    deadlock_errors = 0
    max_gap = -math.inf
    edges_checked = 0

    for u in edges:
        for v in edges[u]:
            edges_checked += 1
            h_u = game.heuristic(u)
            h_v = game.heuristic(v)

            if h_v == math.inf or h_v == float("inf"):
                continue
            if (h_u == math.inf or h_u == float("inf")) and h_v < math.inf:
                deadlock_errors += 1
                continue

            gap = h_u - (cost_per_step + h_v)
            if gap > max_gap:
                max_gap = gap

            if gap > 1e-6:
                consistency_violations += 1

    h_star = {}
    rev_queue = deque()

    for g in goal_states:
        h_star[g] = 0
        rev_queue.append(g)

    while rev_queue:
        s = rev_queue.popleft()
        curr_dist = h_star[s]

        for pred in reverse_edges.get(s, []):
            if pred not in h_star:
                h_star[pred] = curr_dist + cost_per_step
                rev_queue.append(pred)

    admissible_violations = 0
    states_verified = 0

    for state in all_states:
        if state in h_star:
            states_verified += 1
            h_val = game.heuristic(state)
            hs = h_star[state]
            if h_val > hs:
                admissible_violations += 1

    
    bad_violations = 0
    for state in all_states:
        if state in h_star:
            h_bad = 2 * game.heuristic(state)
            if h_bad > h_star[state] and h_star[state] > 0:
                bad_violations += 1

    return {
        "states": len(all_states),
        "edges": edges_checked,
        "cons_violations": consistency_violations,
        "max_gap": max_gap if max_gap != -math.inf else 0.0,
        "solvable_states": states_verified,
        "admiss_violations": admissible_violations,
        "bad_violations": f"{bad_violations}/{states_verified}",
        "status": "PASSED" if (consistency_violations == 0 and admissible_violations == 0) else "FAILED"
    }


if __name__ == "__main__":
    map_files = [
        "maps/example_map.txt",
        "maps/map2.txt",
        "maps/map3.txt",
        "maps/map4.txt",
        "maps/map5.txt",
    ]

    results = []

    print("plese wait...\n")

    for map_file in map_files:
        if not os.path.exists(map_file):
            results.append({"map": os.path.basename(map_file), "status": "not found"})
            continue

        try:
            game = Sokoban(map_file)
            data = run_heuristic_verification(game=game, state_limit=15000,cost_per_step=1)
           
            data["map"] = os.path.basename(map_file)
            results.append(data)
            print(f" done: {os.path.basename(map_file)}")
        except Exception as e:
            results.append({"map": os.path.basename(map_file), "status": f"ERROR: {e}"})

    print("\n" + "=" * 105)
    print("                 SUMMARY TABLE OF HEURISTIC PROPERTIES"      )
    print("=" * 105)
    header = (
        f"{'Map':<16} | {'Edges (|E|)':<11} | {'Cons Viol':<10} | "
        f"{'Max Gap':<8} | {'Solvable (|V|)':<14} | {'Admiss Viol':<12} | {'Control (h_bad)':<18} | {'Status'}"
    )
    print(header)
    print("-" * 105)

    for r in results:
        status_str = str(r.get("status", "")).upper()
        if "ERROR" in status_str or status_str == "NOT FOUND" or "edges" not in r:
            print(f"{r.get('map', 'Unknown'):<16} | {status_str}")
            continue

        row = (
            f"{r['map']:<16} | "
            f"{r['edges']:<10} | "
            f"{r['cons_violations']:<12} | "
            f"{r['max_gap']:<8.2f} | "
            f"{r['solvable_states']:<14} | "
            f"{r['admiss_violations']:<14} | "
            f"{r['bad_violations']:<17} | "
            f"[{r['status']}]"
        )
        print(row)

    print("=" * 105)
    