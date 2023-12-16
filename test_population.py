import unittest

import population


class TestPop(unittest.TestCase):
    # check for a parent id in the range 0-2
    def testSelPar(self):
        fits = [2.5, 1.2, 3.4]
        fit_map = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fit_map)
        self.assertLess(pid, 3)

    # parent id should be 1 as the first fitness is zero
    # second is 1000 and the third is 0.1, so second should
    # almost always be selected
    def testSelPar2(self):
        fits = [0, 1000, 0.1]
        fit_map = population.Population.get_fitness_map(fits)
        pid = population.Population.select_parent(fit_map)
        self.assertEqual(pid, 1)


unittest.main()
