#!/usr/bin/env python

"""Tests for `acdh_arche_pyutils.utils` module."""

import unittest
from acdh_arche_pyutils.utils import (
    camel_to_snake,
    create_query_sting,
    id_from_uri
)


class Test_pyutils_client(unittest.TestCase):
    """Tests for `acdh_arche_pyutils.utils` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_convert_camel_case(self):
        strings = [
            'CamelCase',
            'camel_Case',
            'camel_case',
        ]
        should_be = 'camel_case'
        for x in strings:
            self.assertEqual(camel_to_snake(x), should_be)

    def test_002_create_query_sting(self):
        query_params = {
            "p[0]": "http://www.w3.org/syntax-ns#type",
            "v[0]": "https://schema#TopCollection"
        }
        should_be = 'p[0]=http://www.w3.org/syntax-ns%23type&v[0]=https://schema%23TopCollection'
        self.assertEqual(create_query_sting(query_params), should_be)

    def test_003_id_from_uri(self):
        uris = [
            ['https://schema#TopCollection/123', '123'],
            ['https://schema#TopCollection/123/', '123'],
            ['https://schema#TopCollection/', '']
        ]
        for x in uris:
            self.assertEqual(
                id_from_uri(x[0]),
                x[1],
                f'{x[0]} should become {x[1]}'
            )
