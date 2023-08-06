import unittest
from unittest.mock import patch
import json

from tests.utils import fixtures_path, get_citations, clean_actors, clean_bibliography
from hestia_earth.extend_bibliography.bibliography_apis.unpaywall import extend_unpaywall, extend_bibliography_pdf


class FakeGetRequest():
    def __init__(self, type='search'):
        with open(f"{fixtures_path}/unpaywall/{type}-response.json", 'r') as f:
            self.content = json.load(f)

    def json(self):
        return self.content


def get_exception(): raise Exception('error')


class TestUnpaywall(unittest.TestCase):
    @patch('requests.get', return_value=FakeGetRequest())
    def test_extend_unpaywall(self, _m):
        with open(f"{fixtures_path}/unpaywall/results.json", 'r') as f:
            expected = json.load(f)
        (actors, bibliographies) = extend_unpaywall(get_citations())
        # actor ids are all random, so update result to make sure tests are passing
        result = list(map(clean_actors(expected), actors)) + list(map(clean_bibliography, bibliographies))
        self.assertEqual(result, expected)

    @patch('requests.get', side_effect=get_exception)
    def test_extend_unpaywall_exception(self, _m):
        self.assertEqual(extend_unpaywall(['title']), ([], []))

    def test_extend_bibliography_pdf_no_doi(self):
        bibliography = {}
        result = extend_bibliography_pdf(bibliography)
        self.assertEqual(result, bibliography)

    @patch('requests.get', return_value=FakeGetRequest('doi'))
    def test_extend_bibliography_pdf_with_doi(self, _m):
        bibliography = {'doi': '10.1117/1.jbo.18.2.026003'}
        result = extend_bibliography_pdf(bibliography)
        self.assertEqual(result, {
            **bibliography,
            'articlePdf': 'http://europepmc.org/articles/pmc3556647?pdf=render'
        })


if __name__ == '__main__':
    unittest.main()
