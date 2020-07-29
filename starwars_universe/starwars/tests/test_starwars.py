import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from graphene.test import Client

from django.contrib.auth import get_user_model
from graphql_jwt.testcases import JSONWebTokenTestCase

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
create_character_mutation = """
    mutation CreateCharacter($input: CharacterInput!){
        createCharacter(characterData: $input) {
            character{
                id
                name
            }
            ok
        }
    }
"""
character_filter_query = """
    query($name:String!){
        allCharacters(name_Icontains:$name){
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
        allCharacters {
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
class TestSchema(JSONWebTokenTestCase):
    def setUp(self):
        """Define initial params. """
        #self.client = Client(schema)
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_create_planet(self):
        """Test function to create a planet. """

        print('def test_create_planet')
        payload = {
            "name": "Umbara"
        }
        response = self.client.execute(create_planet_mutation, variables={"input": payload})
        print('Response: ', response)
        print("Response.data: ", response.data)
        print("Response.data.get(createPlanet): ", response.data.get("createPlanet"))
        planet = response.data.get("createPlanet").get("planet")
        name = planet.get("name")
        assert name == payload["name"]

    def test_create_movie(self):
        """Test function to create a movie. """

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
        movie = response.data.get("createMovie").get("movie")
        name = movie.get("name")
        assert name == payload["name"]

    def test_create_character(self):
        """Test function to create a character. """

        print('def test_create_character')
        movie1 = mixer.blend(Movie)
        movie2 = mixer.blend(Movie)
        payload = {
            "name": "Anakin Skywalker",
            "movies": [
                {"id": movie1.id},
                {"id": movie2.id}
            ]
        }
        response = self.client.execute(create_character_mutation, variables={"input": payload})
        print('Response: ', response)
        print('Response.data: ', response.data)
        character = response.data.get("createCharacter").get("character")
        name = character.get("name")
        assert name == payload["name"]
    
    def test_character_filter_query(self):
        """Function that tests a character query with name filter. """
        
        print('def test_character_filter_query')
        character = mixer.blend(Character)
        response = self.client.execute(character_filter_query, variables={"name": character.name })
        print('Response: ', response)
        response_character = response.data.get("allCharacters").get("edges")
        for i in response_character:
            assert i['node']["name"] == str(character.name)

    def test_all_list_query(self):
        """Function that tests a query of all the characters with the respective films in which they appeared and these in turn with their planets. """
        
        print('def test_all_list_query')
        mixer.blend(Character)
        mixer.blend(Character)
        response = self.client.execute(all_list_query)
        print('Response: ', response)
        character = response.data.get("allCharacters").get("edges")
        assert len(character)
