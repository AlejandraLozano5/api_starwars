import graphene
from graphene_django import DjangoObjectType

from .models import *

class PlanetType(DjangoObjectType):
    class Meta:
        model = Planet

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class PersonageType(DjangoObjectType):
    class Meta:
        model = Personage

class Query(graphene.ObjectType):
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


