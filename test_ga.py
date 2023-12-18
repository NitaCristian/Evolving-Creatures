import unittest

import numpy as np

from creature import Creature
from genome import Genome
from population import Population
from simulation import ThreadedSim


class TestGA(unittest.TestCase):
    def test_basic_ga(self):
        pop = Population(pop_size=15, gene_count=5)
        sim = ThreadedSim(pool_size=5)
        # sim = simulation.Simulation()

        for iteration in range(500):
            sim.eval_population(pop, 2400)
            fits = [cr.get_distance_travelled() for cr in pop.creatures]
            links = [len(cr.get_expanded_links()) for cr in pop.creatures]
            print(
                iteration,
                "fittest:",
                np.round(np.max(fits), 3),
                "mean:",
                np.round(np.mean(fits), 3),
                "mean links",
                np.round(np.mean(links)),
                "max links",
                np.round(np.max(links)),
            )
            fit_map = Population.get_fitness_map(fits)
            new_creatures = []
            for i in range(len(pop.creatures)):
                p1_ind = Population.select_parent(fit_map)
                p2_ind = Population.select_parent(fit_map)
                p1 = pop.creatures[p1_ind]
                p2 = pop.creatures[p2_ind]
                # now we have the parents!
                dna = Genome.crossover(p1.dna, p2.dna)
                dna = Genome.point_mutate(dna, rate=0.1, amount=0.25)
                dna = Genome.shrink_mutate(dna, rate=0.25)
                dna = Genome.grow_mutate(dna, rate=0.1)
                cr = Creature(1)
                cr.update_dna(dna)
                new_creatures.append(cr)
            # elitism
            max_fit = np.max(fits)
            for cr in pop.creatures:
                if cr.get_distance_travelled() == max_fit:
                    new_cr = Creature(1)
                    new_cr.update_dna(cr.dna)
                    new_creatures[0] = new_cr
                    filename = "output/elite_" + str(iteration) + ".csv"
                    Genome.to_csv(cr.dna, filename)
                    break

            pop.creatures = new_creatures

        self.assertNotEqual(fits[0], 0)


if __name__ == "__main__":
    unittest.main()
