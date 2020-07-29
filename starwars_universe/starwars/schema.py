import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError

from starwars.models import *

class PlanetNode(DjangoObjectType):
    """Class to define the node interface for the planet model. """
    class Meta:
        model = Planet
        filter_fields = ['name']
        interfaces = (relay.Node, )

class MovieNode(DjangoObjectType):
    """Class to define the node interface for the movie model. """
    class Meta:
        model = Movie
        filter_fields = ['name']
        interfaces = (relay.Node, )

class CharacterNode(DjangoObjectType):
    """Class to define the node interface for the character model. """
    class Meta:
        model = Character
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )

# FOR QUERYS
class Query(graphene.ObjectType):
    """Class to define the querys of the starwars application"""
    
    planet = relay.Node.Field(PlanetNode)
    all_planets = DjangoFilterConnectionField(PlanetNode)

    movie = relay.Node.Field(MovieNode)
    all_movies = DjangoFilterConnectionField(MovieNode)


    character = relay.Node.Field(CharacterNode)
    all_characters = DjangoFilterConnectionField(CharacterNode)


class PlanetInput(graphene.InputObjectType):
    """Class to define input arguments for planet mutation. """
    
    id = graphene.ID()
    name = graphene.String(required=True)

class MovieInput(graphene.InputObjectType):
    """Class to define input arguments for movie mutation. """

    id = graphene.ID()
    name = graphene.String()
    opening_text = graphene.String()
    planets = graphene.List(PlanetInput)
    director = graphene.String()
    producer = graphene.String()

class CharacterInput(graphene.InputObjectType):
    """Class to define input arguments for character mutation. """
    id = graphene.ID()
    name = graphene.String()
    movies = graphene.List(MovieInput)

#FOR MUTATIONS
class CreatePlanet(graphene.Mutation):
    """Class to define the mutation that creates a planet. """
    class Arguments:
        planet_data = PlanetInput(required=True)

    ok = graphene.Boolean()
    planet = graphene.Field(PlanetNode)

    @staticmethod
    def mutate(root, info, planet_data=None):
        print('Doing mutation of PLANET')
        user = info.context.user
        print('User: ', user)
        if user.is_anonymous:
            print('Authentication is required')
            raise GraphQLError('You must be authenticated to create a planet!')

        planet = Planet.objects.create(name=planet_data.name)
        ok = True
        return CreatePlanet(planet=planet, ok=ok)


class CreateMovie(graphene.Mutation):
    """Class to define the mutation that creates a movie. """
    class Arguments:
        movie_data = MovieInput(required=True)
    
    ok = graphene.Boolean()
    movie = graphene.Field(MovieNode)

    @staticmethod
    def mutate(root, info, movie_data=None):
        print('Doing mutation of MOVIE')
        user = info.context.user
        print('User: ', user)
        if user.is_anonymous:
            print('Authentication is required')
            raise GraphQLError('You must be authenticated to create a movie!')

        ok = True
        planets = []
        for planet_input in movie_data.planets:
            planet = Planet.objects.get(name=planet_input.name)
            #planet = Planet.objects.get(id=planet_input.id)
            if planet is None:
                return CreateMovie(movie=None, ok=False)
            planets.append(planet)
        movie = Movie.objects.create(name=movie_data.name, opening_text=movie_data.opening_text, director=movie_data.director, producer=movie_data.producer)
        movie.planets.set(planets)
        
        return CreateMovie(movie=movie, ok=ok)


class CreateCharacter(graphene.Mutation):
    """Class to define the mutation that creates a character. """
    class Arguments:
        character_data = CharacterInput(required=True)
    
    ok = graphene.Boolean()
    character = graphene.Field(CharacterNode)

    @staticmethod
    def mutate(root, info, character_data=None):
        print('Doing mutation of CHARACTER')

        user = info.context.user
        print('User: ', user)
        if user.is_anonymous:
            print('Authentication is required')
            raise GraphQLError('You must be authenticated to create a character!')

        ok = True
        movies = []
        for movie_input in character_data.movies:
            movie = Movie.objects.get(id=movie_input.id)
            if movie is None:
                return CreateCharacter(character=None, ok=False)
            movies.append(movie)
        character = Character.objects.create(name=character_data.name)
        character.movies.set(movies)
        
        return CreateCharacter(character=character, ok=ok)

class Mutation(graphene.ObjectType):
    """ Mutations for starwars app. """
    create_planet = CreatePlanet.Field()
    create_movie = CreateMovie.Field()
    create_character = CreateCharacter.Field()

