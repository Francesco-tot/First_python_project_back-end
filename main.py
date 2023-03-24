
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


app.title = "mi aplicación con FastAPI"
app.version = "0.0.1"

movies = [
    {
    "id":1,
    "title":"Avatar",
    "overview": "En un Exuberante planeta llamado pandora donde viven los navi's",
    "year": "2009",
    "rating": 7.8,
    "category": "Accion" 
    },
    {
    "id":2,
    "title":"Pinocho",
    "overview": "Nino de madera que tiene un ada madrina y se le vuela al cucho",
    "year": "2000",
    "rating": 8.8,
    "category": "Aventura" 
    }
]

@app.get("/",tags = ['home'],response_class = HTMLResponse)
def message():
    return HTMLResponse('<h1>hello world</h1>')

@app.get('/movies',tags = ['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}',tags=['movies'])
def get_movie(id : int):
    movie = list(filter(lambda x:x['id']==id,movies))
    if len(movie) == 0:
        return f'Pelicula no encontrada, ID : {id}'
    return movie

@app.get('/movies/',tags=['movies'])
def get_movie_by_cathegory(category : str, year = ""):
    if year == "":
        moviese = list(filter(lambda x: x['category'] == category,movies))
    else:
        moviese = list(filter(lambda x: x['category'] == category and x['year'] == year,movies))
    if len(movies) == 0:
        return f'Category not allowed'
    return moviese

@app.post('/movies',tags = ['movies'])
def create_movie(title:str,overview:str,year:str,rating:int,category):
    new = {'id':len(movies)+1,'title':title,'overview':overview,'year':year,'rating':rating,'category':category}
    movies.append(new)
    return new['id']

