# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCharacterFunctions::test_all_character 1'] = {
    'data': {
        'allCharacters': [
            {
                'actor': {
                    'name': 'Daniel Radcliffe'
                },
                'house': 'gryffindor',
                'id': '1400',
                'name': 'Harry Potter',
                'wand': {
                    'core': 'pheonix feather',
                    'wood': 'holly'
                }
            },
            {
                'actor': {
                    'name': 'Rupert Grint'
                },
                'house': 'gryffindor',
                'id': '1401',
                'name': 'Ronald Weasley',
                'wand': {
                    'core': 'unicorn tail hair',
                    'wood': 'ash'
                }
            },
            {
                'actor': {
                    'name': 'Emma Watson'
                },
                'house': 'gryffindor',
                'id': '1402',
                'name': 'Hermione Granger',
                'wand': {
                    'core': 'dragon heartstring',
                    'wood': 'vine wood'
                }
            },
            {
                'actor': {
                    'name': 'Ray Fearon'
                },
                'house': None,
                'id': '1403',
                'name': 'Firenze (the centaur)',
                'wand': None
            },
            {
                'actor': {
                    'name': 'Toby Jones'
                },
                'house': None,
                'id': '1404',
                'name': 'Dobby (the elf)',
                'wand': None
            }
        ]
    }
}

snapshots['TestCharacterFunctions::test_character_appears_in 1'] = {
    'data': {
        'characterAppearsIn': [
            {
                'id': '1400',
                'name': 'Harry Potter'
            },
            {
                'id': '1401',
                'name': 'Ronald Weasley'
            },
            {
                'id': '1402',
                'name': 'Hermione Granger'
            },
            {
                'id': '1403',
                'name': 'Firenze (the centaur)'
            }
        ]
    }
}

snapshots['TestCharacterFunctions::test_create_character 1'] = {
    'data': {
        'createCharacter': {
            'character': {
                'appearsIn': [
                    {
                        'id': '1300',
                        'title': "Harry Potter and the Sorcerer's Stone"
                    },
                    {
                        'id': '1301',
                        'title': 'Harry Potter and the Chamber of Secrets'
                    },
                    {
                        'id': '1302',
                        'title': 'Harry Potter and the Prisoner of Azkaban'
                    },
                    {
                        'id': '1303',
                        'title': 'Harry Potter and the Goblet of Fire'
                    },
                    {
                        'id': '1304',
                        'title': 'Harry Potter and the Order of the Phoenix'
                    },
                    {
                        'id': '1305',
                        'title': 'Harry Potter and the Half-Blood Prince'
                    },
                    {
                        'id': '1306',
                        'title': 'Harry Potter and the Deathly Hallows: Part 1'
                    },
                    {
                        'id': '1307',
                        'title': 'Harry Potter and the Deathly Hallows: Part 2'
                    }
                ],
                'id': '1405',
                'name': 'Hagrid'
            }
        }
    }
}

snapshots['TestCharacterFunctions::test_default_character 1'] = {
    'data': {
        'character': {
            'actor': {
                'id': '1200',
                'name': 'Daniel Radcliffe'
            },
            'house': 'gryffindor',
            'id': '1400',
            'name': 'Harry Potter',
            'wand': {
                'core': 'pheonix feather',
                'description': 'nice and supple',
                'id': '1100',
                'length': 11.0,
                'wood': 'holly'
            }
        }
    }
}

snapshots['TestWandFunctions::test_default_wand_full 1'] = {
    'data': {
        'wand': {
            'core': 'pheonix feather',
            'description': 'nice and supple',
            'id': '1100',
            'length': 11.0,
            'wood': 'holly'
        }
    }
}

snapshots['TestWandFunctions::test_default_wand_id 1'] = {
    'data': {
        'wand': {
            'id': '1100'
        }
    }
}

snapshots['TestWandFunctions::test_specific_wand 1'] = {
    'data': {
        'wand': {
            'core': 'pheonix feather',
            'description': 'nice and supple',
            'id': '1100',
            'length': 11.0,
            'wood': 'holly'
        }
    }
}

snapshots['TestCharacterFunctions::test_create_character 2'] = {
    'data': {
        'character': {
            'id': '1405'
        }
    }
}
