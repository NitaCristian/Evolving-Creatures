import creature
import numpy as np


class Population:
    def __init__(self, pop_size, gene_count):
        self.creatures = [creature.Creature(
            gene_count=gene_count)
            for _ in range(pop_size)]

    @staticmethod
    def get_fitness_map(fits):
        fit_map = []
        total = 0
        for f in fits:
            total = total + f
            fit_map.append(total)
        return fit_map

    @staticmethod
    def select_parent(fit_map):
        r = np.random.rand()  # 0-1
        r = r * fit_map[-1]
        for i in range(len(fit_map)):
            if r <= fit_map[i]:
                return i
