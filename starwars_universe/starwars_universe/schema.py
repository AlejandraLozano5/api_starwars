import graphene

from starwars_universe.apps.starwars import schema

class Query(schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)