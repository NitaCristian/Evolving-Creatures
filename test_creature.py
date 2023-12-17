import unittest

import pybullet as p

from creature import Creature, Motor


class TestCreature(unittest.TestCase):
    def test_creature_exists(self):
        self.assertIsNotNone(Creature)

    def test_creature_get_flat_links(self):
        c = Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def test_expanded_links(self):
        c = Creature(gene_count=25)
        links = c.get_flat_links()
        exp_links = c.get_expanded_links()
        self.assertGreaterEqual(len(exp_links), len(links))

    def test_to_xml_not_none(self):
        c = Creature(gene_count=2)
        xml_str = c.to_xml()
        self.assertIsNotNone(xml_str)

    def test_load_xml(self):
        c = Creature(gene_count=20)
        xml_str = c.to_xml()
        with open('models/test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('models/test.urdf')
        self.assertIsNotNone(cid)

    def test_motor_exists(self):
        m = Motor(0.1, 0.5, 0.5)
        self.assertIsNotNone(m)

    def test_motor_output(self):
        m = Motor(0.1, 0.5, 0.5)
        self.assertEqual(m.get_output(), 1)

    def test_motor_output2(self):
        m = Motor(0.6, 0.5, 0.5)
        m.get_output()
        m.get_output()
        self.assertGreater(m.get_output(), 0)

    def test_distance_travelled(self):
        c = Creature(3)
        c.update_position((0, 0, 0))
        d1 = c.get_distance_travelled()
        c.update_position((1, 1, 1))
        d2 = c.get_distance_travelled()
        self.assertGreater(d2, d1)


if __name__ == '__main__':
    unittest.main()
