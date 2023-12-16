import os
import unittest

import numpy as np

import genome


class GenomeTest(unittest.TestCase):
    def test_class_exists(self):
        self.assertIsNotNone(genome.Genome)

    def test_random_gene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def test_random_gene_not_none(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def test_random_gene_has_values(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def test_random_gene_length(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)

    def test_rand_gene_is_numpy_arrays(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def test_random_genome_exists(self):
        data = genome.Genome.get_random_genome(20, 5)
        self.assertIsNotNone(data)

    def test_gene_spec_exist(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def test_gene_spec_has_link_length(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])

    def test_gene_spec_has_link_length_ind(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length']["ind"])

    def test_gene_spec_scale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec["link-length"]["ind"]], 0)

    def test_gene_to_gene_dict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn("link-recurrence", gene_dict)

    def test_genome_to_dict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def test_flat_links(self):
        links = [
            genome.URDFLink(name="A", parent_name=None, recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=2),
            genome.URDFLink(name="C", parent_name="B", recur=2)
        ]
        self.assertIsNotNone(links)

    def test_expand_links(self):
        links = [
            genome.URDFLink(name="A", parent_name="None", recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1),
        ]
        exp_links = [links[0]]
        genome.Genome.expand_links(links[0], links[0].name, links, exp_links)
        self.assertEqual(len(exp_links), 6)

    def test_crossover(self):
        g1 = [[1], [2], [3]]
        g2 = [[4], [5], [6]]
        for i in range(10):
            g3 = genome.Genome.crossover(g1, g2)
            self.assertGreater(len(g3), 0)

    def test_point_mutate(self):
        g1 = np.array([[1.0], [2.0], [3.0]])
        g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
        self.assertFalse(np.array_equal(g1, g2))

    def test_point_mutate_range(self):
        g1 = np.array([[1.0], [0.0], [1.0], [0.0]])
        for i in range(100):
            g2 = genome.Genome.point_mutate(g1, rate=1, amount=0.25)
            self.assertLessEqual(np.max(g2), 1.0)
            self.assertGreaterEqual(np.min(g2), 0.0)

    def test_shrink_mutate(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should definitely shrink as rate = 1
        self.assertEqual(len(g2), 1)

    def test_shrink_mutate2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=0.0)
        # should not shrink as rate = 0
        self.assertEqual(len(g2), 2)

    def test_shrink_mutate3(self):
        g1 = np.array([[1.0]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1.0)
        # should not shrink if already len 1
        self.assertEqual(len(g2), 1)

    def test_grow_mutate1(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        self.assertGreater(len(g2), len(g1))

    def test_grow_mutate2(self):
        g1 = np.array([[1.0], [2.0]])
        g2 = genome.Genome.grow_mutate(g1, rate=0)
        self.assertEqual(len(g2), len(g1))

    def test_to_csv(self):
        g1 = [[1, 2, 3]]
        genome.Genome.to_csv(g1, 'test.csv')
        self.assertTrue(os.path.exists('test.csv'))

    def test_to_csv_content(self):
        g1 = [[1, 2, 3]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n"
        with open('test.csv') as f:
            csv_str = f.read()
        self.assertEqual(csv_str, expect)

    def test_to_csv_content2(self):
        g1 = [[1, 2, 3], [4, 5, 6]]
        genome.Genome.to_csv(g1, 'test.csv')
        expect = "1,2,3,\n4,5,6,\n"
        with open('test.csv') as f:
            csv_str = f.read()
        self.assertEqual(csv_str, expect)

    def test_from_csv(self):
        g1 = [[1, 2, 3]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))

    def test_from_csv2(self):
        g1 = [[1, 2, 3], [4, 5, 6]]
        genome.Genome.to_csv(g1, 'test.csv')
        g2 = genome.Genome.from_csv('test.csv')
        print(g1, g2)
        self.assertTrue(np.array_equal(g1, g2))


if __name__ == "__main__":
    unittest.main()
