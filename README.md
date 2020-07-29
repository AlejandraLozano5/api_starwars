
# api_starwars
A GraphQL and Django project about the starwars universe.
### Run project 
```shell
git clone https://github.com/AlejandraLozano5/api_starwars.git
cd api_starwars
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
cd starwars_universe
python manage.py runserver
```
### Run query and mutation tests
In the folder /starwars_universe check that you have the file "pytest.ini" in that location and then run the following command:

```shell
py.test -s
```

### Testing in Insomnia
For the following requests use the following endpoint: http://127.0.0.1:8000/graphql/`

1) Create a user.
```shell
mutation{
  createUser(
    username:"alejandraa",
    email:"marialelozano@hotmail.com",
    password: "a12345"
    
  ){
    user{
      id
      username
      email
    }
  }
}
```

2) Generate a token for the created user.
```shell
mutation{
  tokenAuth(username:"alejandra", password:"a12345"){
    token
  }
}
```
3) With the token generated in the previous step , in the "Hearder" area of the request in Insomnia, put:
```shell
Content-Type -> application/json
Authorization -> JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFsZWphbmRyYSIsImV4cCI6MTU5NjAzMTU2NSwib3JpZ0lhdCI6MTU5NjAzMTI2NX0.sGOFpJ4D3j76u9wl9Xx0FOlPIZF_O7uULoI30mKB19A

```

Keep the token configured in this way in order to perform the following examples:


  #### All the characters with their movies and these with their planets
  ```shell
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
  ```

  #### All the movies and these with their planets
  ```shell
  query {
    allMovies{
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
  ```
  #### All planets
  You can change "allPlanets" to "allMovies" or "allCharacters" to list only the name of all movies or characters.
  ```shell
  query {
    allPlanets{
      edges {
        node {
          name
        }
      }
    }    
  }
  ```

  #### Filtering
  Filtering the characters that contain the word "Skywalker" in the name
  ```shell
  query {
    allCharacters(name_Icontains: "Skywalker") {
      edges {
        node {
          id
          name
        }
      }
    }
  }
  ```

  #### Creating planets 
  Creating the planet "Umbara" with the mutation.

  ```shell
  mutation CreatePlanet{
    createPlanet(planetData:{name:"Umbara"}){
      planet{
        id
        name
      }
      ok
    }  
  }
  ```

  #### Creating Movies 
  Creating the movie "Start Wars: Episodio I - La amenaza fantasma" and associating their planets by the name.
  ```shell
  mutation createMovie {
    createMovie(movieData: {
      name: "Start Wars: Episodio I - La amenaza fantasma"
      openingText: "La República Galáctica está sumida en el caos. Los impuestos de las rutas comerciales a los sistemas estelares exteriores están en disputa.  Esperando resolver el asunto con un bloqueo de poderosas naves de guerra, la codiciosa Federación de Comercio ha detenido todos los envíos al pequeño planeta de Naboo.  Mientras el Congreso de la República debate interminablemente esta alarmante cadena de acontecimientos, el Canciller Supremo ha enviado en secreto a dos Caballeros Jedi, guardianes de la paz y la justicia en la galaxia, para resolver el conflicto...."
      producer:"Rick McCallum"
      director:"George Lucas"
      planets:[
        {name: "Umbara"},
        {name: "Anoat"}
      ]
    }) {
      movie{
        name
      }
      ok
    }
  }
  ```
  #### Creating Characters 
  Creating the character "Anakin Skywalker" and associating their planets using the id
  ```shell
  mutation createCharacter {
    createCharacter(characterData: {
      name: "Anakin Skywalker"
      movies:[
        {id: 1},
        {id: 2}
      ]
    }) {
      character{
        name
      }
      ok
    }
  }
  ```
