# Sokoban AI

Midterm Project for the **503043 – Introduction to Artificial Intelligence** course at **Ton Duc Thang University**.

## Project Overview

This project focuses on applying **Artificial Intelligence search techniques** to the Sokoban puzzle.

In the first part, Sokoban is formulated as a **state-space search problem** and solved using **Uniform Cost Search (UCS)** and **A* Search**. A heuristic is proposed for A*, and experiments are conducted to compare the performance of the two algorithms and evaluate the heuristic.

In the second part, the traditional Sokoban problem is extended into a **competitive two-agent environment**. Two AI agents play on the same map, compete for boxes and destinations, and make decisions within a limited amount of time.

## Project Requirements

### Req 1 – State-Space Formulation

Formulate Sokoban as a state-space search problem by defining the **state, initial state, available actions, goal state, and path cost**.

The objective is to find a sequence of actions that moves the boxes from their initial positions to the required destinations.

### Req 2 – UCS and A* Search

Implement two search algorithms for solving Sokoban:

- Uniform Cost Search (UCS)
- A* Search

A heuristic function is proposed for A* to estimate the remaining cost to reach the goal. Euclidean and Manhattan distance are not used as the proposed heuristic.

### Req 3 – Performance Experiment

Conduct experiments to compare **UCS and A*** in terms of time and space complexity.

The comparison considers information such as execution time, explored or expanded states, memory usage, and solution cost on different Sokoban maps.

### Req 4 – Heuristic Analysis

Analyze the proposed heuristic and verify two important properties:

- **Admissibility:** the heuristic does not overestimate the optimal remaining cost.
- **Consistency:** the heuristic satisfies the consistency condition between neighboring states.

Experiments are also performed to support the analysis.

### Req 5 – Pygame Visualization

Develop a graphical interface using **Pygame** to visualize the Sokoban solution.

The user can select UCS or A*, view the number of actions, pause or resume the solution, and move forward or backward through the generated states.

### Req 6 – Competitive Two-Agent Sokoban

Extend the original Sokoban problem into a **competitive environment with two agents**.

Both agents act simultaneously and compete to place boxes on destinations. The user specifies the maximum number of steps `n`, and the agent with more completed boxes after `n` steps wins.

A box placed on a destination can still be moved by the other agent, allowing agents to compete for completed boxes.

### Req 7 – Competitive AI Agents

Develop AI algorithms to control the two competitive agents.

Each agent observes the current game state, selects an action, and must complete its decision within **1000 milliseconds**.

### Req 8 – Competitive Gameplay

Develop the competitive gameplay using **Pygame**.

The interface visualizes both agents, boxes, destinations, box ownership, scores, current steps, and the final result.

The algorithms controlling Agent 1 and Agent 2 are stored in separate source files so that different agents can be tested or compared.

## Technologies

- Python
- Pygame
- Uniform Cost Search (UCS)
- A* Search
- Heuristic Search
- Competitive AI Agents

## Project Goal

The main goal of this project is to demonstrate how AI search techniques can be applied to both a **single-agent search problem** and a **competitive two-agent problem**.

The project combines search algorithms, heuristic analysis, performance experiments, and graphical visualization to study how different AI approaches behave in Sokoban.

## Course Information

**Course:** 503043 – Introduction to Artificial Intelligence  
**University:** Ton Duc Thang University  
**Project:** Midterm Project – Sokoban AI