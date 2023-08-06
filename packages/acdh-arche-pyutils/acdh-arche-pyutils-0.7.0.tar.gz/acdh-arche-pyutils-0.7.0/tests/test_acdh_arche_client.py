# #!/usr/bin/env python

# """Tests for `acdh_arche_pyutils.client` module."""
import os
import unittest
from acdh_arche_pyutils.client import ArcheApiClient


class Test_pyutils_client(unittest.TestCase):
    """Tests for `acdh_arche_pyutils.client` module."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.endpoint = "https://arche-dev.acdh-dev.oeaw.ac.at/api/"
        self.arche_client = ArcheApiClient(self.endpoint, out_dir='./out')
        self.top_col = self.arche_client.top_col_ids()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_parse_url(self):
        self.assertEqual(self.arche_client.endpoint, self.endpoint)

    def test_002_get_description(self):
        description = self.arche_client.description
        self.assertEqual(type(description), dict)

    def test_003_populate_client_props(self):
        for x in ['id', 'parent', 'modification_date']:
            self.assertTrue(hasattr(self.arche_client, x))

    def test_004_base_url_match(self):
        a_cl = self.arche_client
        self.assertEqual(a_cl.endpoint, a_cl.fetched_endpoint)

    def test_005_top_cols(self):
        self.assertTrue(isinstance(self.top_col, list))
        self.assertEqual(len(self.top_col[0]), 2)

    def test_006_get_resource(self):
        some_uri = self.top_col[0][0]
        res = self.arche_client.get_resource(some_uri)
        self.assertTrue("rdfg:Graph" in f"{res}")

    def test_007_write_resource_to_file(self):
        some_uri = self.top_col[0][0]
        print(some_uri)
        res = self.arche_client.write_resource_to_file(some_uri)
        self.assertTrue(os.path.isfile(res))
        # res_xml = self.arche_client.write_resource_to_file(some_uri, format='xml')
        # self.assertTrue(res_xml.endswith('.xml'))
        os.remove(res)
