import sys
from graphene import (ObjectType, Enum, ID, String, Float, List, Field, Schema,)
from pymongo import MongoClient
from itertools import combinations


# def combine_factorially(val):
#     # print("==%s=="%(val), file=sys.stderr)
#     for x in reversed(range(len(val.items()))):
#         # print("==%s=="%(x+1), file=sys.stderr)
#         comb = combinations(val, x+1) 
#         for c in comb: yield c
# print("==%s=="%("Hello"), file=sys.stderr)


client = MongoClient('localhost', 27017)
db = client.harry_potter_trivia


class House(Enum):
    gryffindor = "GRYFFINDOR"
    hufflepuff = "HUFFLEPUFF"
    ravenclaw = "RAVENCLAW"
    slytherin = "SLYTHERIN"


class Wand(ObjectType):
    id = ID()
    wood = String(required=True)
    core = String(required=True)
    length = Float(required=True)
    description = String() 


class Actor(ObjectType):
    id = ID()
    name = String(required=True) 


class Movie(ObjectType):
    id = ID()
    title = String(required=True)
    release_date = String()


class Character(ObjectType):
    id = ID()
    name = String(required=True)
    appears_in = List(lambda: Movie)
    actor = Field(lambda: Actor, required=True)
    house = String()
    wand = Field(lambda: Wand)


class Query(ObjectType):
    wand = Field(Wand, id=ID(), wood=String(), core=String())
    actor = Field(Actor, id=ID(), name=String())
    movie = Field(Movie, id=ID(), title=String(), release_date=String())
    character = Field(Character, 
        id=ID(), 
        name=String(), 
        appears_in=String(), 
        actor=String(), 
        house=House(), 
        wand_core=String(),
        )

    def resolve_wand(self, info, **args):
        def fill_out(d):
            if d is not None:
                return Wand(
                    id=d['id'], 
                    wood=d['wood'], 
                    core=d['core'], 
                    length=d['length'], 
                    description=d['description'],
                    )
            else:
                return None

        if len(args):
            return fill_out(db.wands.find_one(args))
        else:
            return fill_out(db.wands.find_one({'id': '1100'}))

    def resolve_actor(self, info, **args):
        def fill_out(d):
            if d is not None:
                return Actor(
                    id=d['id'], 
                    name=d['name'], 
                    )
            else:
                return None

        if len(args):
            return fill_out(db.actors.find_one(args))
        else:
            return fill_out(db.actors.find_one({'id': '1200'}))

    def resolve_movie(self, info, **args):
        def fill_out(d):
            if d is not None:
                return Movie(
                    id=d['id'], 
                    title=d['title'], 
                    release_date=d['release_date'], 
                    )
            else:
                return None

        if len(args):
            return fill_out(db.movies.find_one(args))
        else:
            return fill_out(db.movies.find_one({'id': "1300"}))

    def resolve_character(self, info, **args) :
        def fill_out(d):
            if d is not None:
                return Character(
                    id=d['id'], 
                    name=d['name'], 
                    appears_in=d['appears_in'], 
                    actor=d['actor'], 
                    house=d['house'],
                    wand_core=d['wand_core'],
                    )
            else:
                return None

        if len(args):
            return fill_out(db.characters.find_one(args))
        else:
            return fill_out(db.characters.find_one({'id': "1400"}))
    

schema = Schema(query=Query)


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

    # print(db.actors.find_one({'id': harrypotter_actor.id}))

if __name__ == "__main__":
    setup()