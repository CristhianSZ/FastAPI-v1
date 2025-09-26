from http.client import HTTPException
from fastapi import Depends, FastAPI, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken, validateToken
from fastapi.security import HTTPBearer
from bd.database import Session, engine, Base
from models.movie import Movie







app = FastAPI(
    title='Aprendiendo FastApi',
    description='Una api en los primeros pasos',
    version='0.0.1'
)

Base.metadata.create_all(bind=engine)


class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(
                status_code=403, detail='Credenciales incorrectas')


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula',
                       min_length=5, max_length=30)
    overview: str = Field(
        default='Descripcion de la pelicula', min_length=5, max_length=50)
    year: int = Field(default=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=15)


movies = [
    {
        'id': 1,
        'title': 'El Padrino',
        'overview': "El Padrino es una película de 1972 dirigida por Francis For Coppola ...",
        'year': '1972',
        'rating': 9.2,
        'category': 'Crimen'
    }
]


@app.post('/login', tags=['authentication'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "123":
        token: str = createToken(user.model_dump())
        return JSONResponse(content={'token': token})


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


@app.get("/", tags=['inicio'], status_code=200)
def read_root():
    """ No solo se puede responder con un objeto, tambien se pueden responder con etiquetas HTML """
    """ return {"message": "Hello World"} """
    return HTMLResponse('<h2> Hola Mundo! </h2>')


""" Se genera un endpoint para traer todas las peliculas """


@app.get("/movies", tags=['Get Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    return movies


""" Parametos de ruta """
""" Cuando se esta haciendo la peticion tambien hay que considerar el caso de que no llegue el dato que tipo de dato enviar. """


@app.get('/movies/{id}', tags=['Get Movie'], status_code=200)
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


@app.post('/movies', tags=['Movies'], status_code=201)
def create_movies(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={'message': 'Se ha cargado una nueva pelicula', 'movies': [movie.model_dump() for m in movies]})


""" Metodo PUT y DELETE """


@app.put('/movies/{id}', tags=['Movies'], status_code=200)
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={'message': 'Se ha modificado la pelicula'})
    return []


@app.delete('/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={'message': 'Se ha eliminado la pelicula'})
    return []
