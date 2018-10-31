import sys
from graphene import ObjectType, Enum, ID, String, Float, List, Field, Schema
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


# ===== HELPER FUNCTIONS =====
def fill_out(objecttype_class, d):
    if d is None:
        return None
    if '_id' in d:
        _ = d.pop('_id')
    return objecttype_class(**d)


# ===== OBJECTTYPE DEFINITIONS =====
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
    house = Field(House)
    wand = Field(lambda: Wand)

    def resolve_appears_in(self, info):
        movie_list = [db.movies.find_one({'id': a}) for a in self.appears_in]
        movie_list = [fill_out(Movie, m) for m in movie_list]
        return movie_list

    def resolve_actor(self, info):
        this_actor = db.actors.find_one({'id': self.actor})
        this_actor = fill_out(Actor, this_actor)
        return this_actor

    def resolve_wand(self, info):
        this_wand = db.wands.find_one({'id': self.wand})
        this_wand = fill_out(Wand, this_wand)
        return this_wand


# ===== QUERY DEFINITION =====
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
        wand=String(),
        )

    def res_decorator(func):
        def wrapper(*args, **kwargs):
            objecttype_class, db_con, args, default_id = func(*args, **kwargs)
            if len(args):
                return fill_out(objecttype_class, db_con.find_one(args))
            else:
                return fill_out(objecttype_class, db_con.find_one({'id': default_id}))
        return wrapper

    @res_decorator
    def resolve_wand(self, info, **args):
        return Wand, db.wands, args, '1100'

    @res_decorator
    def resolve_actor(self, info, **args):
        return Actor, db.actors, args, '1200'

    @res_decorator
    def resolve_movie(self, info, **args):
        return Movie, db.movies, args, '1300'

    @res_decorator
    def resolve_character(self, info, **args) :
        return Character, db.characters, args, '1400'
    

schema = Schema(query=Query)