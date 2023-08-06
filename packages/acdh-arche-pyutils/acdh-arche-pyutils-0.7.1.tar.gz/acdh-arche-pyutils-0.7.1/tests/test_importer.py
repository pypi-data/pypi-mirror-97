#!/usr/bin/env python

"""Tests for `acdh_arche_pyutils.client.Importer` class."""
import unittest
from acdh_arche_pyutils.client import ArcheToTripleStore


class Test_pyutils_importer(unittest.TestCase):
    """Tests for `acdh_arche_pyutils.client` module."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.endpoint = "https://arche-dev.acdh-dev.oeaw.ac.at/api/"
        self.triple_store = "https://some-fake-url"
        self.client = ArcheToTripleStore(
            self.triple_store,
            arche_endpoint=self.endpoint
        )
        self.top_ids = self.client.top_col_ids()
        self.res_id = self.top_ids[0][0]

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_test_init(self):
        self.assertEqual(self.client.endpoint, self.endpoint)
        self.assertEqual(self.client.triple_store, self.triple_store)

    def test_002_get_res_id(self):
        self.assertIsInstance(self.res_id, str)

    def test_003_post(self):
        response = self.client.post_resource(self.res_id)
        self.assertIsInstance(response, list)

    # def test_0004_triplescount(self):
    #     self.assertIsInstance(self.client.count_triples(), int)
