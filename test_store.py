import unittest, tempfile
from pathlib import Path
from store import IncidentStore, Conflict

class StoreTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'incidents.db'
        self.store = IncidentStore(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_persistence(self):
        self.store.create('Fictional API outage', 'API', 'High')
        self.assertEqual(IncidentStore(self.path).list()[0]['state'], 'Open')

    def test_atomic_rejected_transition(self):
        r = self.store.create('Outage', 'API', 'High')
        with self.assertRaises(ValueError):
            self.store.move(r['id'], 'Closed', 1, 'skip')
        self.assertEqual(len(self.store.list()[0]['history']), 1)

    def test_retry_idempotence(self):
        r = self.store.create('Outage', 'API', 'High')
        a = self.store.move(r['id'], 'Investigating', 1, 'a')
        b = self.store.move(r['id'], 'Investigating', 1, 'a')
        self.assertEqual(a, b)
        self.assertEqual(len(b['history']), 2)

    def test_stale_writer(self):
        r = self.store.create('Outage', 'API', 'High')
        self.store.move(r['id'], 'Investigating', 1, 'first')
        with self.assertRaises(Conflict):
            self.store.move(r['id'], 'Resolved', 1, 'second')

    def test_request_key_misuse(self):
        r = self.store.create('Outage', 'API', 'High')
        self.store.move(r['id'], 'Investigating', 1, 'first')
        with self.assertRaises(Conflict):
            self.store.move(r['id'], 'Resolved', 2, 'first')
