import unittest

import population


class TestPopulation(unittest.TestCase):
    # Check for a parent id in the range 0-2
    def test_select_parent(self):
        fits = [2.5, 1.2, 3.4]
        fit_map = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fit_map)
        self.assertLess(pid, 3)

    # Parent id should be 1 as the first fitness is zero,
    # the second is 1000, and the third is 0.1, so the second should
    # almost always be selected
    def test_select_parent2(self):
        fits = [0, 1000, 0.1]
        fit_map = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fit_map)
        self.assertEqual(pid, 1)


if __name__ == "__main__":
    unittest.main()
