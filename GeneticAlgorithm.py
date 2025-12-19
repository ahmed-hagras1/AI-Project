import random
import math

class GeneticAlgorithm:
    def __init__(self, maze, population_size=100, mutation_rate=0.05, generations=500, heuristic_type="manhattan"):
        self.maze = maze.grid
        self.n = maze.n
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.heuristic_type = heuristic_type.lower() # Store the heuristic choice
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
        self.chromosome_length = self.n * self.n 

    def create_individual(self):
        return [random.choice(self.directions) for _ in range(self.chromosome_length)]

    def get_path_from_individual(self, individual):
        path = [(0, 0)]
        x, y = 0, 0
        
        for move in individual:
            dx, dy = move
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < self.n and 0 <= ny < self.n and self.maze[nx][ny] == 0:
                x, y = nx, ny
                path.append((x, y))
                if (x, y) == (self.n - 1, self.n - 1):
                    break
            else:
                break 
                
        return path

    def calculate_distance(self, current, goal):
        """Helper method to calculate distance based on chosen heuristic."""
        x1, y1 = current
        x2, y2 = goal
        
        if self.heuristic_type == "manhattan":
            return abs(x1 - x2) + abs(y1 - y2)
        elif self.heuristic_type == "euclidean":
            return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        elif self.heuristic_type == "chebyshev":
            return max(abs(x1 - x2), abs(y1 - y2))
        else:
            return 0

    def fitness(self, individual):
        path = self.get_path_from_individual(individual)
        final_pos = path[-1]
        goal = (self.n - 1, self.n - 1)
        
        # USE THE DYNAMIC CALCULATION HERE
        dist = self.calculate_distance(final_pos, goal)
        
        # Max distance reference needs to be large enough for any heuristic
        max_dist = 2 * self.n 
        
        score = max_dist - dist
        
        if final_pos == goal:
            score += 100
            score += (self.chromosome_length - len(path))
            
        return max(0, score) # Ensure score isn't negative

    def selection(self, population, fitnesses):
        selected = []
        for _ in range(self.pop_size):
            i, j = random.randint(0, self.pop_size-1), random.randint(0, self.pop_size-1)
            if fitnesses[i] > fitnesses[j]:
                selected.append(population[i])
            else:
                selected.append(population[j])
        return selected

    def crossover(self, parent1, parent2):
        if random.random() < 0.7: 
            point = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] = random.choice(self.directions)
        return individual

    def solve(self, start=(0,0), goal=None):
        population = [self.create_individual() for _ in range(self.pop_size)]
        total_individuals_evaluated = 0
        
        best_solution = []
        solved = False

        for gen in range(self.generations):
            fitness_scores = [self.fitness(ind) for ind in population]
            total_individuals_evaluated += len(population)
            
            max_fit = max(fitness_scores)
            best_ind = population[fitness_scores.index(max_fit)]
            
            if max_fit >= 100:
                best_solution = self.get_path_from_individual(best_ind)
                solved = True
                break
            
            selected_pop = self.selection(population, fitness_scores)
            
            next_pop = []
            for i in range(0, self.pop_size, 2):
                p1 = selected_pop[i]
                p2 = selected_pop[i+1] if i+1 < len(selected_pop) else selected_pop[0]
                
                c1, c2 = self.crossover(p1, p2)
                next_pop.append(self.mutate(c1))
                next_pop.append(self.mutate(c2))
            
            population = next_pop

        if not solved:
            fitness_scores = [self.fitness(ind) for ind in population]
            best_ind = population[fitness_scores.index(max(fitness_scores))]
            best_solution = self.get_path_from_individual(best_ind)

        return best_solution, total_individuals_evaluated