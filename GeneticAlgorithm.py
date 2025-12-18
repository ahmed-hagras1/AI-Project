import random

class GeneticAlgorithm:
    def __init__(self, maze, population_size=100, mutation_rate=0.05, generations=500):
        self.maze = maze.grid
        self.n = maze.n
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
        # Chromosome length roughly equal to maze area gives enough room for a path
        self.chromosome_length = self.n * self.n 

    def create_individual(self):
        """Creates a random sequence of moves (genes)."""
        return [random.choice(self.directions) for _ in range(self.chromosome_length)]

    def get_path_from_individual(self, individual):
        """
        Translates a list of moves into a list of coordinates (path).
        Stops if it hits a wall or goes out of bounds.
        """
        path = [(0, 0)]
        x, y = 0, 0
        
        for move in individual:
            dx, dy = move
            nx, ny = x + dx, y + dy
            
            # Check bounds and walls
            if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                x, y = nx, ny
                path.append((x, y))
                # Stop if goal reached
                if (x, y) == (self.n - 1, self.n - 1):
                    break
            else:
                # If hit wall/boundary, stop this path (simple implementation)
                # or just ignore the move (stay in place). 
                # Stopping usually helps convergence by penalizing invalid paths heavily.
                break 
                
        return path

    def fitness(self, individual):
        """
        Calculates fitness score.
        Higher is better.
        """
        path = self.get_path_from_individual(individual)
        final_pos = path[-1]
        goal = (self.n - 1, self.n - 1)
        
        # Distance to goal (Manhattan)
        dist = abs(final_pos[0] - goal[0]) + abs(final_pos[1] - goal[1])
        
        # Base score is inverse of distance
        # Max distance is 2*n. We want score to be high when dist is low.
        max_dist = 2 * self.n
        score = max_dist - dist
        
        # Big Bonus for actually reaching the goal
        if final_pos == goal:
            score += 100
            # Bonus for shorter paths
            score += (self.chromosome_length - len(path))
            
        return score

    def selection(self, population, fitnesses):
        """Tournament Selection: Pick 2 random, choose best."""
        selected = []
        for _ in range(self.pop_size):
            i, j = random.randint(0, self.pop_size-1), random.randint(0, self.pop_size-1)
            if fitnesses[i] > fitnesses[j]:
                selected.append(population[i])
            else:
                selected.append(population[j])
        return selected

    def crossover(self, parent1, parent2):
        """Single Point Crossover."""
        if random.random() < 0.7: # 70% chance to crossover
            point = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(self, individual):
        """Randomly changes genes."""
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] = random.choice(self.directions)
        return individual

    def solve(self, start=(0,0), goal=None): # Args kept for consistency, though handled internally
        """
        Runs the genetic algorithm loop.
        """
        population = [self.create_individual() for _ in range(self.pop_size)]
        total_individuals_evaluated = 0
        
        best_solution = []
        solved = False

        for gen in range(self.generations):
            # 1. Calculate Fitness
            fitness_scores = [self.fitness(ind) for ind in population]
            total_individuals_evaluated += len(population)
            
            # Check for best solution in this generation
            max_fit = max(fitness_scores)
            best_ind = population[fitness_scores.index(max_fit)]
            
            # If we found a path to the goal (score > 100 based on our formula)
            if max_fit >= 100:
                best_solution = self.get_path_from_individual(best_ind)
                solved = True
                break
            
            # 2. Selection
            selected_pop = self.selection(population, fitness_scores)
            
            # 3. Crossover & Mutation (Create new population)
            next_pop = []
            for i in range(0, self.pop_size, 2):
                p1 = selected_pop[i]
                p2 = selected_pop[i+1] if i+1 < len(selected_pop) else selected_pop[0]
                
                c1, c2 = self.crossover(p1, p2)
                next_pop.append(self.mutate(c1))
                next_pop.append(self.mutate(c2))
            
            population = next_pop

        # If loop finishes without solving, take the closest one found
        if not solved:
             # Recalculate best of final generation
            fitness_scores = [self.fitness(ind) for ind in population]
            best_ind = population[fitness_scores.index(max(fitness_scores))]
            best_solution = self.get_path_from_individual(best_ind)

        return best_solution, total_individuals_evaluated