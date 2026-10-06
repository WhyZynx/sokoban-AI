import csv
import os
import time
import tracemalloc
from pathlib import Path
from sokoban import Sokoban, search 
BASE_DIR = Path(__file__).resolve().parent
MAPS_DIR = BASE_DIR / "maps"
RESULTS_FILE = BASE_DIR / "benchmark_results.csv"

NUM_RUNS = 3  
ALGORITHMS = [("UCS", False), ("A*", True)]


def get_compatible_maps():
    if not MAPS_DIR.exists():
        print(f"Directory '{MAPS_DIR}' not found.")
        return []

    map_paths = sorted(MAPS_DIR.glob("*.txt"))
    
    return [p for p in map_paths if p.name != "competitive_map.txt"]


def run_benchmark():
    maps = get_compatible_maps()
    if not maps:
        print("No valid map files found for testing.")
        return

    records = []
    print(f"{'Map':<18} | {'Algo':<5} | {'Cost':<5} | {'Expanded':<9} | {'Max Frontier':<12} | {'Avg Time (s)':<12} | {'Peak RAM (MB)':<13} | {'Status'}")
    print("-" * 88)

    for map_path in maps:
        map_name = map_path.name

        for algo_name, use_astar in ALGORITHMS:
            times = []
            last_actions = None
            last_cost = 0
            last_expanded = 0
            last_max_frontier = 0
            num_boxes = 0

            
            for _ in range(NUM_RUNS):
                game = Sokoban(str(map_path))
                num_boxes = len(game.initial[1])

                t_start = time.perf_counter()
                actions, cost, expanded, max_frontier, _ = search(game, use_astar=use_astar, return_all=True)
                t_elapsed = time.perf_counter() - t_start

                times.append(t_elapsed)
                last_actions = actions
                last_cost = cost
                last_expanded = expanded
                last_max_frontier = max_frontier

            avg_time = sum(times) / len(times)

         
            tracemalloc.start()
            game_mem = Sokoban(str(map_path))
            search(game_mem, use_astar=use_astar, return_all=True)
            _, peak_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            peak_mb = peak_bytes / (1024 * 1024)

            is_success = last_actions is not None
            status = "SUCCESS" if is_success else "FAIL"
            cost_display = str(last_cost) if is_success else "N/A"

            print(f"{map_name:<18} | {algo_name:<5} | {cost_display:<5} | {last_expanded:<9} | {last_max_frontier:<12} | {avg_time:<12.4f} | {peak_mb:<13.4f} | {status}")

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

    fieldnames = ["Map", "Boxes", "Algorithm", "Success", "Cost", "Expanded", "Max_Frontier", "Avg_Time_s", "Peak_RAM_MB"]
    with open(RESULTS_FILE, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(records)

    print("-" * 88)
    print(f"Benchmark completed! Results have been saved to: {RESULTS_FILE.name}")

if __name__ == "__main__":
    run_benchmark()