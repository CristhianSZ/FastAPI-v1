from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI(
    title='Aprendiendo FastApi',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(default='Titulo de la pelicula', min_length=5, max_length=15)
    overview : str =  Field(default='Descripcion de la pelicula', min_length=5, max_length=15)
    year : int = Field(default=2022)
    rating : float = Field(ge=1, le=10)
    category : str = Field(min_length=3, max_length=15)





movies = [
    {
        'id' : 1,
        'title' : 'El Padrino',
        'overview' : "El Padrino es una película de 1972 dirigida por Francis For Coppola ...",
        'year' : '1972',
        'rating' : 9.2,
        'category' : 'Crimen'
    }
]



"""Documentacion automatica: al agregar dontro de la instancia atributos, como title, description y version se puede modificar la documentacion
para acceder a la documentacion se ingresar en la  url/docs
en los verbos HTTP se pueden agregar las etiquetas para personalizar la documentacion con tags 
En la documentacion puedo ver la informacion de los enpoints la ver Response """


""" Metodos HTTP; indica que se quiere hacer con un recurso determinado del servidor
POST: crear un recurso nuevo
PUT: modificar un recurso existente
GET: consultar informacion de un recurso.
DELETE: eliminar un recurso. """


""" 
METODO GET

 """

@app.get("/", tags=['inicio'])
def read_root():
    """ No solo se puede responder con un objeto, tambien se pueden responder con etiquetas HTML """
    """ return {"message": "Hello World"} """
    return HTMLResponse('<g2> Hola Mundo! </h2>')

""" Se genera un endpoint para traer todas las peliculas """
@app.get("/movies", tags=['Get Movies'])
def get_movies():
    return movies


""" Parametos de ruta """
""" Cuando se esta haciendo la peticion tambien hay que considerar el caso de que no llegue el dato que tipo de dato enviar. """

@app.get('/movies/{id}', tags=['Get Movie'])
def get_movie(id: int = Path(ge=1, le=100)):
    for item in movies:
        if item["id"] == id:
            return item
    return []

""" Parametro de Query """
""" A diferencia del caso anterior FastAPI intulle que es una busqueda por query """
@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=3, max_length=15)):
    return category


""" Metodo POST """

@app.post('/movies', tags=['Movies'])
def create_movies(movie: Movie):
    movies.append(movie)
    print(movies)
    return movies

""" Metodo PUT y DELETE """

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id : int , movie: Movie ):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return movies
    return []
    

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    return []

