# Introduction to Artificial Intelligence - Programming Assignment 4

## Decision-making under uncertainty - MAPD Problem

This repository contains the solution to Programming Assignment 4, which focuses on sequential decision making under uncertainty using belief-state Markov Decision Processes (MDP). The problem scenario is akin to the Canadian Traveler Problem but with additional uncertainties.

### Goals
The main objective of this assignment is to develop a solution for decision-making in the MAPD (Multi-Agent Pathfinding with Delivery) problem, which involves finding optimal policies for delivering a package through a grid-based graph with uncertain blockages.

### MAPD Delivery Decision Problem - Domain Description
In this problem, we are given a grid-based undirected graph where each edge has a known probability of being blocked. The agent's task is to deliver a package from a start vertex to a target vertex, with the added challenge of uncertain blockages. The true state of a fragile edge remains constant, and the goal is to find a policy that minimizes delivery time in expectation.

### Solution Method
The solution employs belief-state MDPs and value iteration to compute the optimal policy. The belief space is stored explicitly in memory, with a limit of grid size at most 6 by 6 and 10 possible uncertain blockages. The program initializes belief space value functions and iteratively computes the value function for belief states, maintaining the optimal action for each state.


### Deliverables
- Source code 
- Explanation of the algorithm in the README below.
- Example runs on different scenarios in Example_runs.txt

### How to Run
To run the program, ensure you have Python 3 installed. Then execute the following command:
- python3 main.py --file <input_file_path>

Replace `<input_file_path>` with the path to your input file containing graph information. The program will read this file, compute the optimal policy, and provide output accordingly.


### Explanation of the algorithm 
- __Shortly we solve it in the same method in test.__

The solution method involves a pragmatic approach to decision-making under uncertainty, 
specifically tailored to address the challenges posed by the MAPD (Multi-Agent Pathfinding with Delivery) problem.

- State Representation:

Each edge in the grid-based graph is associated with a binary state, indicating whether it is believed to be blocked or unblocked. Additionally, an "unknown" state denoted by "U" represents uncertainty about the state of an edge.
Expected Value Computation:

For each edge, two states are considered: one where the edge is assumed to be blocked, and one where it is assumed to be unblocked (the opposite state).
The expected value for each edge is then computed by considering the possible outcomes of each state (e.g., delivery time) and weighting them by their respective probabilities.
Policy Determination:

Based on the computed expected values for each edge,
decisions are made on which actions to take in the belief-state space.
The agent selects actions that maximize the expected utility, considering the uncertainty represented by the "unknown" state.
