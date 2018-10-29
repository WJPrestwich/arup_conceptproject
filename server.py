from flask import Flask
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView
# from schema import schema

class Query(ObjectType):
    hello = String(description="Hello")
    def resolve_hello(self, info):
        return "World"

app = Flask(__name__)
app.add_url_rule(
    "/", 
    view_func=GraphQLView.as_view("graphql", schema=Schema(query=Query), graphiql=True)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)