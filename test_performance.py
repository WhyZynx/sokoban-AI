import sys
import time

from competitive import CompetitiveGame, load_competitive_map

from agents.agent1 import Agent1
from agents.agent2 import Agent2


MAP_PATH = "maps/competitive_map.txt"

(
    walls,
    boxes,
    destinations,
    agent1_position,
    agent2_position,
    height,
    width
) = load_competitive_map(MAP_PATH)

game = CompetitiveGame(
    walls,
    boxes,
    destinations,
    agent1_position,
    agent2_position,
    100,
    height,
    width
)

agent1 = Agent1()
agent2 = Agent2()

agent1_times = []
agent2_times = []


print("PERFORMANCE TEST")


for step in range(20):
    if game.is_finished():
        break
    print("Step:", step + 1)


    start = time.perf_counter()
    action1 = agent1.choose_action(game)
    end = time.perf_counter()
    time1 = end - start
    agent1_times.append(time1)

    start = time.perf_counter()
    action2 = agent2.choose_action(game)
    end = time.perf_counter()
    time2 = end - start
    agent2_times.append(time2)

    print(
        "Agent 1:",
        action1,
        f"{time1:.6f}s"
    )

    print(
        "Agent 2:",
        action2,
        f"{time2:.6f}s"
    )


    game.step(action1, action2)


print("\nPERFORMANCE RESULT")

max_agent1 = max(agent1_times)
max_agent2 = max(agent2_times)

avg_agent1 = sum(agent1_times) / len(agent1_times)
avg_agent2 = sum(agent2_times) / len(agent2_times)


print(
    "Agent 1 max:",
    f"{max_agent1:.6f}s"
)

print(
    "Agent 1 average:",
    f"{avg_agent1:.6f}s"
)

print(
    "Agent 2 max:",
    f"{max_agent2:.6f}s"
)

print(
    "Agent 2 average:",
    f"{avg_agent2:.6f}s"
)

passed = True

if max_agent1 <= 1.0:
    print("Agent 1: PASS")
else:
    print("Agent 1: FAIL")
    passed = False

if max_agent2 <= 1.0:
    print("Agent 2: PASS")
else:
    print("Agent 2: FAIL")
    passed = False

if not passed:
    sys.exit(1)