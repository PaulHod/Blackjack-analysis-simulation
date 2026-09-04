from Genetic_Algorithm.genome import Genome
import random
import numpy as np
import time

set = []

# Create a list of 10 random strategies

for j in range(50):
    current = Genome()
    current_hard = np.zeros(100, dtype=int)
    current_soft = np.zeros(80, dtype=int)
    current_pairs = np.zeros(100, dtype=int)
    random.seed(time.time())
    for i in range(100):
        current_hard[i] = random.randint(0,2)
    for i in range(80):
        current_soft[i] = random.randint(0,2)
    for i in range(100):
        current_pairs[i] = random.randint(0,3)
    current.assign(current_hard, current_soft, current_pairs)
    set.append(current)

# Analyze and score each strategy
# Normalize scores
# Create 10 new genomes from scores:

best = []
for i in range(1000):
    print(f"Starting generation {i}")
    scores = np.zeros_like(set, dtype=float)
    for index, graph in enumerate(set):
        scores[index] = graph.analyze(10000,5)
    scores = scores - scores.min()
    total = scores.sum()
    scores = scores/total # Normalize scores 0-1
    indexes = np.zeros_like(scores)
    indexes[0] = scores[0]
    for index in range(np.size(indexes))[1:]:
        indexes[index] = indexes[index-1] + scores[index]
    best.append(set[np.argmax(scores)]) # Create indexing for later random decisions
    best[-1].write(f"best_of_gen_{i}_50_ind.json")

    new_set = []
    for j in range(50):
        current = Genome()
        current_hard = np.zeros(100, dtype=int)
        current_soft = np.zeros(80, dtype=int)
        current_pairs = np.zeros(100, dtype=int)
        for square in range(100):
            choice = random.random()
            index = np.searchsorted(indexes, choice, side="right")
            current_hard[square] = set[index].linearize()[0][square]
        for square in range(80):
            choice = random.random()
            index = np.searchsorted(indexes, choice, side="right")
            current_soft[square] = set[index].linearize()[1][square]
        for square in range(100):
            choice = random.random()
            index = np.searchsorted(indexes, choice, side="right")
            current_pairs[square] = set[index].linearize()[2][square]
        current.assign(current_hard, current_soft, current_pairs)
        new_set.append(current)
    set = new_set
    
best[-1].display()
