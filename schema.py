import sys
from graphene import ObjectType, Enum, ID, String, Float, List, Field, Mutation, Schema
from pymongo import MongoClient
from itertools import combinations


client = MongoClient("mongodb://mongodb:27200")
db = client.harry_potter_trivia


# ===== HELPER FUNCTIONS =====
# We'll pass in a class type to instantiate our ObjectType dynamically.
def fill_out(objecttype_class, d):
    if d is None:
        return None
    if '_id' in d:
        _ = d.pop('_id')
    return objecttype_class(**d)


# This allows us to print to the Flask std out.
def debug_print(msg):
    print("==%s=="%(msg), file=sys.stderr)


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
        actor=String(), 
        house=House(), 
        wand=String(),
        )
    character_appears_in = Field(List(Character), appears_in=ID(required=True))

    # We'll use a decorator here to cut down on similar code.
    def res_decorator(func):
        def wrapper(*args, **kwargs):
            objecttype_class, db_con, args, default_id = func(*args, **kwargs)
            if len(args):
                # If given some arguments, search based on those.
                return fill_out(objecttype_class, db_con.find_one(args))
            else:
                # If no search parameters are given, fetch the first instance.
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

    def resolve_character_appears_in(self, info, appears_in):
        temp = db.characters.find({'appears_in': appears_in})
        chars = [fill_out(Character, t) for t in temp]
        return chars
    

# ===== MUTATION DEFINITIONS =====
class CreateCharacter(Mutation):
    class Arguments:
        name = String()
        appears_in = List(ID)
        actor = ID()
        house = House()
        wand = ID()

    character = Field(lambda: Character)

    def mutate(self, info, name, appears_in, actor, house=None, wand=None):
        # This character's id is equal to the last character's id plus one.
        last = db.characters.find_one(sort=[("id", -1)])
        debug_print(last)
        _id = str(int(last['id'])+1)

        result = db.characters.insert_one({
            "id": _id,
            "name": name,
            "appears_in": appears_in,
            "actor": actor,
            "house": house,
            "wand": wand,
        })

        character = Character(
            id = _id,
            name = name,
            appears_in = appears_in,
            actor = actor,
            house = house,
            wand = wand,
        )
        return CreateCharacter(character=character)

class Mutations(ObjectType):
    create_character = CreateCharacter.Field()


schema = Schema(query=Query, mutation=Mutations)