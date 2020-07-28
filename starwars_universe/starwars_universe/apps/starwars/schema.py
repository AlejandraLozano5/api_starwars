import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import *

class PlanetNode(DjangoObjectType):
    class Meta:
        model = Planet
        filter_fields = ['name']
        interfaces = (relay.Node, )

class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = ['name']
        interfaces = (relay.Node, )

class PersonageNode(DjangoObjectType):
    class Meta:
        model = Personage
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node, )
class Query(graphene.ObjectType):
    planet = relay.Node.Field(PlanetNode)
    all_planets = DjangoFilterConnectionField(PlanetNode)

    movie = relay.Node.Field(MovieNode)
    all_movies = DjangoFilterConnectionField(MovieNode)


    personage = relay.Node.Field(PersonageNode)
    all_personages = DjangoFilterConnectionField(PersonageNode)
    
    """
    planets = graphene.List(PlanetType)
    movies = graphene.List(MovieType)
    personages = graphene.List(PersonageType)

    def resolve_planets(self, infor, **kwargs):
        return Planet.objects.all()

    def resolve_movies(self, infor, **kwargs):
        #return Movie.objects.select_related('planet').all()
        return Movie.objects.all()
    
    def resolve_personages(self, infor, **kwargs):
        return Personage.objects.all()
    """

#For mutations
"""
class CreatePlanet(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    planet = graphene.Field(PlanetNode)

    @staticmethod
    def mutate(root, info, name):
        print('Doing mutation of planet')
        #planet = Planet(name=name)  
        planet = Planet.objects.create(name=name)
        ok = True
        return CreatePlanet(planet=planet, ok=ok)
"""
class PlanetInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class CreatePlanet(graphene.Mutation):
    class Arguments:
        planet_data = PlanetInput(required=True)

    ok = graphene.Boolean()
    planet = graphene.Field(PlanetNode)

    @staticmethod
    def mutate(root, info, planet_data=None):
        print('Doing mutation of planet')
        #planet = Planet(name=name)  
        #planet = Planet.objects.create(**planet_data)
        planet = Planet.objects.create(name=planet_data.name)
        ok = True
        return CreatePlanet(planet=planet, ok=ok)

class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    opening_text = graphene.String()
    planets = graphene.List(PlanetInput)
    director = graphene.String()
    producer = graphene.String()

class CreateMovie(graphene.Mutation):
    class Arguments:
        movie_data = MovieInput(required=True)
    
    ok = graphene.Boolean()
    movie = graphene.Field(MovieNode)

    @staticmethod
    def mutate(root, info, movie_data=None):
        print('Doing mutation of MOVIE')
        ok = True
        planets = []
        for planet_input in movie_data.planets:
            planet = Planet.objects.get(name=planet_input.name)
            if planet is None:
                return CreateMovie(movie=None, ok=False)
            planets.append(planet)
        movie = Movie.objects.create(name=movie_data.name, opening_text=movie_data.opening_text, director=movie_data.director, producer=movie_data.producer)
        movie.planets.set(planets)
        
        return CreateMovie(movie=movie, ok=ok)

class PersonageInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    movies = graphene.List(MovieInput)

class CreatePersonage(graphene.Mutation):
    class Arguments:
        personage_data = PersonageInput(required=True)
    
    ok = graphene.Boolean()
    personage = graphene.Field(PersonageNode)

    @staticmethod
    def mutate(root, info, personage_data=None):
        print('Doing mutation of PERSONAGE')
        ok = True
        movies = []
        for movie_input in personage_data.movies:
            movie = Movie.objects.get(id=movie_input.id)
            if movie is None:
                return CreatePersonage(movie=None, ok=False)
            movies.append(movie)
        personage = Personage.objects.create(name=personage_data.name)
        personage.movies.set(movies)
        
        return CreatePersonage(personage=personage, ok=ok)

class MyMutations(graphene.ObjectType):
    create_planet = CreatePlanet.Field()
    create_movie = CreateMovie.Field()
    create_personage = CreatePersonage.Field()

