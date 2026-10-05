import csv
import os
import time
import tracemalloc
from sokoban import Sokoban, search
# def load_map_from_file(file_path):
#     walls = set()
#     goals = set()
#     boxes = set()
#     agent_pos = None

#     with open(file_path, "r", encoding="utf-8") as f:
#         lines = [line.rstrip("\r\n") for line in f.readlines()]
#     # for r, row in enumerate(lines):
#     #         print(r, len(row))
#     for r, row_str in enumerate(lines):
#         for c, char in enumerate(row_str):
#             if char == "%":
#                 walls.add((r, c))
#             elif char == "A":
#                 agent_pos = (r, c)
#             elif char == "B":
#                 boxes.add((r, c))
#             elif char == "D":
#                 goals.add((r, c))
#             elif char == "C":
#                 boxes.add((r, c))
#                 goals.add((r, c))
#     initial_state = (agent_pos, frozenset(boxes))
#     return initial_state, walls, goals
 
def run_experiment_and_export_csv():

    map_files = [
        {"name": "example_map", "path": os.path.join("maps", "example_map.txt")},
        {"name": "map2", "path": os.path.join("maps", "map2.txt")},
        {"name": "map3", "path": os.path.join("maps", "map3.txt")},
        {"name": "map4", "path": os.path.join("maps", "map4.txt")},
        {"name": "map5", "path": os.path.join("maps", "map5.txt")},
    ]

    algorithms = [("UCS", False ), ("A*",True)]
    NUM_RUNS = 3
    # TIMEOUT_SECONDS = 60.0  
    CSV_FILENAME = "benchmark_results.csv"

    records = []

    print(f"{'Map':<15} | {'Algo':<5} | {'Boxes':<5} | {'Cost':<5} | {'Expanded':<9} | {'Avg Time (s)':<12} | {'Peak RAM (MB)':<13} | {'Status'}")
    print("-" * 85)

    for item in map_files:
        map_name = item["name"]
        map_path = item["path"]

        if not os.path.exists(map_path):
            print(f"Không tìm thấy file tại đường dẫn '{map_path}'")
            continue

        for algo_name, use_astar in algorithms:
            times = []
            last_actions = None
            last_cost = 0
            last_expanded = 0
            last_max_frontier = 0

            for _ in range(NUM_RUNS):
                game = Sokoban(map_path)
                
                t_start = time.perf_counter()
                actions, cost, expanded, max_frontier, _ = search(game, use_astar=use_astar)
                t_elapsed = time.perf_counter() - t_start

                times.append(t_elapsed)
                last_actions = actions
                last_cost = cost
                last_expanded = expanded
                last_max_frontier = max_frontier

            avg_time = sum(times) / len(times)

            tracemalloc.start()
            game_mem = Sokoban(map_path)
            search(game_mem, use_astar=use_astar)
            _, peak_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_mb = peak_bytes / (1024 * 1024)
            
            is_success = last_actions is not None
            status = "SUCCESS" if is_success else "FAIL"
            num_boxes = len(game.initial[1])

            print(f"{map_name:<15} | {algo_name:<5} | {num_boxes:<5} | {str(last_cost):<5} | {last_expanded:<9} | {avg_time:<12.4f} | {peak_mb:<13.4f} | {status}")

            records.append({
                "Map": map_name,
                "Boxes": num_boxes,
                "Algorithm": algo_name,
                "Success": is_success,
                "Cost": last_cost,
                "Expanded": last_expanded,
                "Max_Frontier": last_max_frontier,
                "Avg_Time_s": round(avg_time, 4),
                "Peak_RAM_MB": round(peak_mb, 4),
            })

    fieldnames = ["Map", "Boxes", "Algorithm", "Success", "Cost","Expanded",  "Max_Frontier", "Avg_Time_s", "Peak_RAM_MB"]
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames,delimiter=';')
        writer.writeheader()
        writer.writerows(records)

    print("-" * 85)
    print(f"done: {CSV_FILENAME}")


if __name__ == "__main__":
    run_experiment_and_export_csv()