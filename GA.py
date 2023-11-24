# Import libraries
import random
import copy
import numpy as np
from Bird import Bird
from config import *

# Genetic Algorithm
def evolve(generation, history):
    # New Generation Distribution
    total_individuals = int(len(generation))
    # %40 Selection 
    selection_individuals = int((50*total_individuals)/100)
    # %60 Crossover
    crossover_individuals = int(total_individuals-selection_individuals)

    individuals_selected = []
    # ===================================== Selection =====================================
    # Sort the generation by score of each individual
    curr_generation = sorted(generation, key=lambda x: x.score, reverse=True)
    # === Fitness Scaling ===
    new_range = (50,100)
    
    # Lowest fitness value
    max_ = curr_generation[0].score
    # Highest fitness value
    min_ = curr_generation[len(curr_generation)-1].score
    # Solving the linear system ecuations and find the constants
    # For "a"
    if max_-min_ == 0:
        a = (new_range[0])/(1)
    else:
        a = (new_range[0])/(max_-min_)
    # For "b"
    b = new_range[1]-(max_*a)

    roulette = {}
    # Calculate the scaled fitness for each one bird
    total_roulette = 0
    for i in range(len(curr_generation)):
        scaled = int(a * curr_generation[i].score + b)
        roulette[i] = {'Bird':curr_generation[i],'Fitness':curr_generation[i].score ,'Scaled':scaled}
        total_roulette += scaled

    # Re-calculate the portion using the formula of Fitness Scaling
    for item in roulette:
        roulette[item]['Portion'] = round((roulette[item]['Scaled']*100) / total_roulette,2)

    # Rotate the Roulette Wheel 'selection_individuals' times 
    for i in range(selection_individuals):
        # Generate the selection pointer 
        selection_point = random.randint(0,100)
        cummulative = 0 
        # Spin the roulette 
        for item in roulette:
            cummulative += roulette[item]['Portion']
            if selection_point <= cummulative:
                # Copy the object selected to 'new generation'
                individuals_selected.append(copy.deepcopy(curr_generation[item]))
                break

    # === Fitness Scaling ===
    # ===================================== Selection =====================================
    # ===================================== CrossOver =====================================
    # ===================================== (blend crossover) =====================================
    # TODO : cruce uniforme
    # TODO : cruce basado en máscaras

    individuals_crossed = []
    for n in range(crossover_individuals): 
        # Choose two parents randomly
        index_parent_1 = random.randint(0,len(individuals_selected)-1)
        index_parent_2 = random.randint(0,len(individuals_selected)-1)
        while index_parent_1 == index_parent_2:
            index_parent_2 = random.randint(0,len(individuals_selected)-1)

        # We extract the weights from the brain 
        father = individuals_selected[index_parent_1].brain.weights
        mother = individuals_selected[index_parent_2].brain.weights
        offsring = []

        # Calculate alpha for the new offspring random.random()
        alpha = 0.5

        for w in range(len(father)):
            offsring.append(np.zeros(father[w].shape))
            for i in range(father[w].shape[0]):
                for j in range(father[w].shape[1]):
                    offsring[w][i][j] = alpha * father[w][i][j] + (1 - alpha) * mother[w][i][j]

        new_individual = Bird(x=50,
            y=SCREEN_HEIGHT // 2,
            w=50,
            h=30,
            color=random.randint(0,2),
            flap=-12,
            human=False,
            brain=offsring)
        # Add the new offspring to list 
        individuals_crossed.append(new_individual)

    next_generation = individuals_selected + individuals_crossed
    # ===================================== CrossOver =====================================
    # ===================================== Mutation Adaptative =====================================
    long_history = 2
    history = history
    if len(history) < long_history:
        history.append(max_)
        history.append(max_)
    else: 
        history.pop(0)
        history.append(max_)

    mutation_prob = 0.0
    mean = 0 if len(history) == 0 else sum(history)/len(history)

    if (history[1]+history[0])/2 > 200: # Hubo avance significativo
        mutation_prob = 0.1
    elif history[1]-history[0] < 0: # Hubo decremento
        mutation_prob = 0.8
    elif (history[1]+history[0])/2 >= 0 and (history[1]+history[0])/2 < 300: # Necesita o puede mejorar
        mutation_prob = 0.3

    for individual in next_generation:
        for w in range(len(individual.brain.weights)):
            for i in range(individual.brain.weights[w].shape[0]):
                for j in range(individual.brain.weights[w].shape[1]):
                    if random.random() <= mutation_prob:
                        individual.brain.weights[w][i][j] = random.uniform(-1, 1)

    print('Max: {} Mean: {}'.format(max_,mean))
    return (next_generation, history)

    # ===================================== Mutation =====================================


    #print(total_individuals)
    #print(selection_individuals)
    #print(crossover_individuals)