import graphene
import graphql_jwt
import starwars.schema
import users.schema

class Query(starwars.schema.Query, users.schema.Query, graphene.ObjectType):
    pass

class Mutation(starwars.schema.Mutation, users.schema.Mutation, graphene.ObjectType):
    """Mutations for starwars_universe project. """

    #Mutations for authentication
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)