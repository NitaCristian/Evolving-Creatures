import unittest

import creature
import population
import simulation


class TestSim(unittest.TestCase):
    def test_sim_exists(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim)

    def test_sim_id(self):
        sim = simulation.Simulation()
        self.assertIsNone(sim.physicsClientId)  # Adjusted the condition

    def test_run(self):
        sim = simulation.Simulation()
        self.assertIsNotNone(sim.run_creature)

    def test_pos(self):
        sim = simulation.Simulation()
        cr = creature.Creature(gene_count=3)
        sim.run_creature(cr)
        self.assertNotEqual(cr.start_position, cr.last_position)

    def test_pop(self):
        pop = population.Population(pop_size=5, gene_count=3)
        sim = simulation.Simulation()
        for cr in pop.creatures:
            sim.run_creature(cr)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)

    # Uncomment this to test the
    # multi-threaded sim
    #    def test_proc(self):
    #        pop = population.Population(pop_size=20, gene_count=3)
    #        t_sim = simulation.ThreadedSim(pool_size=8)
    #        t_sim.eval_population(pop, 2400)
    #        dists = [cr.get_distance_travelled() for cr in pop.creatures]
    #        print(dists)
    #        self.assertIsNotNone(dists)

    def test_proc_no_thread(self):
        pop = population.Population(pop_size=20, gene_count=3)
        sim = simulation.Simulation()
        sim.eval_population(pop, 2400)
        dists = [cr.get_distance_travelled() for cr in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)


if __name__ == "__main__":
    unittest.main()
