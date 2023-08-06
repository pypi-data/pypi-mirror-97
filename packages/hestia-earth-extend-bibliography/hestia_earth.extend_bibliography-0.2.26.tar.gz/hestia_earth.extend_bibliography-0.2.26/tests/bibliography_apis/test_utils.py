import unittest
import re

from hestia_earth.extend_bibliography.bibliography_apis.utils import actor_id, actor_name, update_actor_names, \
    capitalize


class FakeAuthor():
    def __init__(self):
        self.scopus_author_id = ''


class TestBibliographyUtils(unittest.TestCase):
    def test_actor_id(self):
        actor = {'scopusID': 'scopus_author_id'}
        self.assertEqual(actor_id(actor), actor.get('scopusID'))

        # no scopus, generate random value
        actor = {'scopusID': None}
        self.assertTrue(re.match(r'H-\d{10}$', actor_id(actor)))

    def test_actor_name(self):
        actor = {'lastName': 'Last Name'}
        self.assertEqual(actor_name(actor), 'Last Name')
        actor['firstName'] = 'First'
        self.assertEqual(actor_name(actor), 'F Last Name')
        # override name
        actor['name'] = 'Full Name'
        self.assertEqual(actor_name(actor), 'F Last Name')

    def test_update_actor_names(self):
        first_name = 'L. N. R.'
        last_name = 'Last Name'
        actor = {'firstName': first_name, 'lastName': last_name}
        self.assertEqual(update_actor_names(actor), {
            'firstName': first_name, 'lastName': last_name, 'name': 'L Last Name'
        })
        # invert first/last, should sort them out
        actor = {'firstName': last_name, 'lastName': first_name}
        self.assertEqual(update_actor_names(actor), {
            'firstName': first_name, 'lastName': last_name, 'name': 'L Last Name'
        })

    def test_capitalize(self):
        self.assertEqual(capitalize(None), None)
        self.assertEqual(capitalize('A random title'), 'A random title')
        self.assertEqual(capitalize('A RANDOM TITLE'), 'A Random Title')


if __name__ == '__main__':
    unittest.main()
