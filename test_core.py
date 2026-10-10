import unittest
from core import transition,simulate,run
class Tests(unittest.TestCase):
    def test_transition(self):self.assertEqual(transition('Open','Investigating'),'Investigating')
    def test_skip(self):
        with self.assertRaises(ValueError):transition('Open','Closed')
    def test_terminal(self):
        with self.assertRaises(ValueError):transition('Closed','Open')
    def test_history(self):
        for item in simulate()['incidents']:
            for a,b in zip(item['history'],item['history'][1:]):self.assertGreater(b['minute'],a['minute'])
    def test_count(self):self.assertEqual(len(run({'count':20})['incidents']),20)
