from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(
    title='Aprendiendo FastApi',
    description='Una api en los primeros pasos',
    version='0.0.1'
)
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
def get_movie(id: int):
    for item in movies:
        if item["id"] == id:
            return item
    return []

""" Parametro de Query """
""" A diferencia del caso anterior FastAPI intulle que es una busqueda por query """
@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str):
    return category


""" Metodo POST """

@app.post('/movies', tags=['Movies'])
def create_movies(
    id : int = Body(),
    title : str = Body(),
    overview : str = Body(),
    year : int = Body(),
    rating : float = Body(),
    category : str = Body()
):
    movies.append({
  "id": id,
  "title": title,
  "overview": overview,
  "year": year,
  "rating": rating,
  "category": category
})
    return title

""" Metodo PUT y DELETE """

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(
    id : int,
    title : str = Body(),
    overview : str = Body(),
    year : int = Body(),
    rating : float = Body(),
    category : str = Body()

 ):
    for item in movies:
        if item["id"] == id:
            item['title'] = title
            item['overview'] = overview
            item['year'] = year
            item['rating'] = rating
            item['category'] = category
            return movies
    return []
    

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return movies
    return []

