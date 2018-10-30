import graphene
from pymongo import MongoClient
from pprint import pprint
from schema import (House,Wand,Actor,Movie,Character,)

client = MongoClient('localhost', 27017)
# db = client.admin

# server_status_result = db.command("serverStatus")
# pprint(server_status_result)


db = client.harry_potter_trivia

harrypotter_wand = Wand(
	id = "1100",
	wood = "holly",
	core = "pheonix feather",
	length = 11,
	description = "nice and supple",
)

wands = [
	harrypotter_wand,
]

def setup():
	for w in wands:
		if not db.wands.find({'id': w.id}).count():
			result = db.wands.insert_one({
				"id": w.id,
				"wood": w.wood,
				"core": w.core,
				"length": w.length,
				"description": w.description,
			})

	print(db.wands.find_one({'id': harrypotter_wand.id}))

def get_wand(wood, core):
	return harrypotter_wand


if __name__ == "__main__":
	setup()