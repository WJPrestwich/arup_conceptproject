#!/usr/bin/env python3

import unittest
import snapshottest
import mongomock

from graphene.test import Client
# from snapshottest import TestCase

# Setup our path, to be able to call unit_tests.py directly rather than 
# through packaging and then calling as a module outside of this project.
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import schema
import setup


def mock_database(func):
    '''Sets the mongo client and database to a fresh mocked copy'''

    def wrapper(*args, **kwargs):
        mock_client = mongomock.MongoClient()
        setup.client = mock_client
        setup.setup(quiet=True)
        schema.db = mock_client.harry_potter_trivia

        return func(*args, **kwargs)

    return wrapper


def execute_query(query):
    client = Client(schema.schema)
    return client.execute(query)


class TestWandFunctions(snapshottest.TestCase):

    @mock_database
    def test_default_wand_id(self):
        executed = execute_query('''
            query { 
                wand { 
                    id 
                } 
            }''')

        self.assertMatchSnapshot(executed)

    @mock_database
    def test_default_wand_full(self):
        executed = execute_query('''
            query { 
                wand { 
                    id 
                    wood 
                    core 
                    length 
                    description 
                } 
            }''')

        self.assertMatchSnapshot(executed)

    @mock_database
    def test_specific_wand(self):
        executed = execute_query('''
            query { 
                wand(id: 1100) { 
                    id 
                    wood 
                    core 
                    length 
                    description 
                } 
            }''')

        self.assertMatchSnapshot(executed)

class TestCharacterFunctions(snapshottest.TestCase):

    @mock_database
    def test_default_character(self):
        executed = execute_query('''
            query {
              character {
                id
                name
                actor {
                  id
                  name
                }
                house
                wand {
                  id
                  wood
                  core
                  length
                  description
                }
              }
            }''')

        self.assertMatchSnapshot(executed)

    @mock_database
    def test_all_character(self):
        executed = execute_query('''
            query {
              allCharacters{
                id
                name
                actor{
                  name
                }
                house
                wand{
                  wood
                  core
                }
              }
            }''')

        self.assertMatchSnapshot(executed)

    @mock_database
    def test_character_appears_in(self):
        executed = execute_query('''
            query {
              characterAppearsIn(appearsIn: 1300){
                id
                name
              }
            }''')

        self.assertMatchSnapshot(executed)

    @mock_database
    def test_create_character(self):
        executed = execute_query('''
            mutation createCharacter {
              createCharacter(actor: 1200, appearsIn: [1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307], name: "Hagrid"){
                character{
                  id
                  name
                  appearsIn {
                    id
                    title
                  }
                }
              }
            }''')

        self.assertMatchSnapshot(executed)

        # We also want to test the character exists in the database
        new_id = executed['data']['createCharacter']['character']['id']
        executed = execute_query('''
            query {
              character(id: %s){
                id
              }
            }'''%new_id)
        self.assertMatchSnapshot(executed)



if __name__ == '__main__':
    unittest.main()