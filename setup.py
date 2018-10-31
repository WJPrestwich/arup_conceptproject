from schema import Wand, Actor, Movie, Character
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.harry_potter_trivia

def setup():
    wands = [
        Wand(
            id = "1100",
            wood = "holly",
            core = "pheonix feather",
            length = 11,
            description = "nice and supple",
        ),
    ]

    actors = [
        Actor(
            id = "1200",
            name = "Daniel Radcliffe"
        ),
    ]

    movies = [
        Movie(
            id = "1300",
            title = "Harry Potter and the Sorcerer's Stone",
            release_date = "2001",
        ),
        Movie(
            id = "1301",
            title = "Harry Potter and the Chamber of Secrets",
            release_date = "2002",
        ),
        Movie(
            id = "1302",
            title = "Harry Potter and the Prisoner of Azkaban",
            release_date = "2004",
        ),
        Movie(
            id = "1303",
            title = "Harry Potter and the Goblet of Fire",
            release_date = "2005",
        ),
        Movie(
            id = "1304",
            title = "Harry Potter and the Order of the Phoenix",
            release_date = "2007",
        ),
        Movie(
            id = "1305",
            title = "Harry Potter and the Half-Blood Prince",
            release_date = "2009",
        ),
        Movie(
            id = "1306",
            title = "Harry Potter and the Deathly Hallows: Part 1",
            release_date = "2010",
        ),
        Movie(
            id = "1307",
            title = "Harry Potter and the Deathly Hallows: Part 2",
            release_date = "2011",
        ),
    ]

    characters = [
        Character(
            id = "1400",
            name = "Harry Potter",
            appears_in = ["1300","1301","1302","1303","1304","1305","1306","1307",],
            actor= "1200",
            house = "GRYFFINDOR",
            wand = "1100",
        ),
    ]

    for w in wands:
        if not db.wands.find({'id': w.id}).count():
            result = db.wands.insert_one({
                "id": w.id,
                "wood": w.wood,
                "core": w.core,
                "length": w.length,
                "description": w.description,
            })

    for a in actors:
        if not db.actors.find({'id': a.id}).count():
            result = db.actors.insert_one({
                "id": a.id,
                "name": a.name,
            })

    for m in movies:
        if not db.movies.find({'id': m.id}).count():
            result = db.movies.insert_one({
                "id": m.id,
                "title": m.title,
                "release_date": m.release_date,
            })

    for c in characters:
        if not db.characters.find({'id': c.id}).count():
            result = db.characters.insert_one({
                "id": c.id,
                "name": c.name,
                "appears_in": c.appears_in,
                "actor": c.actor,
                "house": c.house,
                "wand": c.wand,
            })

    # print(db.characters.find_one({'id': '1400'}))

if __name__ == "__main__":
    setup()