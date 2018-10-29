from graphene import ObjectType, String, Schema

class Query(ObjectType):
    hello = String(description="Hello")
    def resolve_hello(self, args, context, info):
        return "World"