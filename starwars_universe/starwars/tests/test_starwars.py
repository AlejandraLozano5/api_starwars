import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from graphene.test import Client

from starwars.models import *
from starwars_universe.schema import schema


create_planet_mutation = """
     mutation CreatePlanet($input: PlanetInput!) {
        createPlanet(planetData: $input) {
            planet{
                id
                name
            }
            ok
        }
    }
"""
create_movie_mutation = """
    mutation CreateMovie($input: MovieInput!){
        createMovie(movieData: $input){
            movie{
                id
                name
            }
            ok
        }
    }
"""
create_personage_mutation = """
    mutation CreatePersonage($input: PersonageInput!){
        createPersonage(personageData: $input) {
            personage{
                id
                name
            }
            ok
        }
    }
"""
personage_filter_query = """
    query($name:String!){
        allPersonages(name_Icontains:$name){
            edges {
                node {
                    id
                    name
                }
            }
        }
    }
"""

all_list_query = """
    query {
        allPersonages {
            edges {
                node {
                    name,
                    movies {
                        edges {
                            node {
                                name,
                                planets {
                                    edges {
                                        node {
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
"""

@pytest.mark.django_db
class TestSchema(TestCase):
    def setUp(self):
        print('SET UP')
        self.client = Client(schema)

    def test_personage_filter_query(self):
        print('def test_personage_filter_query')
        personage = mixer.blend(Personage)
        response = self.client.execute(personage_filter_query, variables={"name": personage.name })
        print('Response: ', response)
        response_personage = response.get("data").get("allPersonages").get("edges")
        for i in response_personage:
            assert i['node']["name"] == str(personage.name)

    def test_all_list_query(self):
        print('def test_all_list_query')
        mixer.blend(Personage)
        mixer.blend(Personage)

        response = self.client.execute(all_list_query)
        print('Response: ', response)
        personage = response.get("data").get("allPersonages").get("edges")
        assert len(personage)

    def test_create_planet(self):
        print('def test_create_planet')
        payload = {
            "name": "Umbara"
        }

        response = self.client.execute(create_planet_mutation, variables={"input": payload})
        print('Response: ', response)
        planet = response.get("data").get("createPlanet").get("planet")
        name = planet.get("name")
        assert name == payload["name"]

    def test_create_movie(self):
        print('def test_create_movie')
        planet1 = mixer.blend(Planet)
        planet2 = mixer.blend(Planet)

        payload = {
            "name": "Episodio I - La amenaza fantasma",
            "openingText": "La República Galáctica está sumida en el caos. Los impuestos de las rutas comerciales a los sistemas estelares exteriores están en disputa.  Esperando resolver el asunto con un bloqueo de poderosas naves de guerra, la codiciosa Federación de Comercio ha detenido todos los envíos al pequeño planeta de Naboo.  Mientras el Congreso de la República debate interminablemente esta alarmante cadena de acontecimientos, el Canciller Supremo ha enviado en secreto a dos Caballeros Jedi, guardianes de la paz y la justicia en la galaxia, para resolver el conflicto....",
            "producer":"Rick McCallum",
            "director":"George Lucas",
            "planets":[
                {"name": planet1.name},
                {"name": planet2.name}
            ]
        }

        response = self.client.execute(create_movie_mutation, variables={"input": payload})
        print('Response: ', response)
        movie = response.get("data").get("createMovie").get("movie")
        name = movie.get("name")
        assert name == payload["name"]

    def test_create_personage(self):
        print('def test_create_personage')
        movie1 = mixer.blend(Movie)
        movie2 = mixer.blend(Movie)

        payload = {
            "name": "Anakin Skywalker",
            "movies": [
                {"id": movie1.id},
                {"id": movie2.id}
            ]
        }
        
        response = self.client.execute(create_personage_mutation, variables={"input": payload})
        print('Response: ', response)
        personage = response.get("data").get("createPersonage").get("personage")
        name = personage.get("name")
        assert name == payload["name"]
