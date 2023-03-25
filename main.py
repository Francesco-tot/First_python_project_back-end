
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from fastapi import Request

app = FastAPI()


app.title = "mi aplicación con FastAPI"
app.version = "0.0.1"

var_movies = [
    {
    "id":1,
    "title":"Avatar",
    "overview": "En un Exuberante planeta llamado pandora donde viven los navi's",
    "year": "2009",
    "rating": "7.8",
    "category": "Accion" 
    },
    {
    "id":2,
    "title":"Pinocho",
    "overview": "Nino de madera que tiene un ada madrina y se le vuela al cucho",
    "year": "2000",
    "rating": "8.8",
    "category": "Aventura" 
    }
]

@app.get("/",tags = ['home'],response_class = HTMLResponse)
def message():
    return HTMLResponse('<h1>Welcome to Movie Practice API :D</h1>')

@app.get('/movies',tags = ['movies'])
def get_movies():
    return var_movies

@app.get('/movies/{id}',tags=['movies'])
def get_movie(id : int):
    movie = list(filter(lambda x:x['id']==id,var_movies))
    if len(movie) == 0:
        return f'Pelicula no encontrada, ID : {id}'
    return movie

@app.get('/movies/year/{year}',tags=['movies'])
def get_movie_by_year(year:str):
    if year == "":
        return []
    moviese = list(filter(lambda x:x['year'] == year,var_movies))
    return moviese

@app.get('/movies/categories/{category}',tags=['movies'])
def get_movie_by_category(category:str):
    if category == "":
        return []
    moviese = list(filter(lambda x:x['category'] == category,var_movies))
    return moviese

@app.get('/movies/rating/{rating}',tags=['movies'])
def get_movie_by_rating(rating:str):
    if rating == "":
        return []
    moviese = list(filter(lambda x:x['rating'] == rating,var_movies))
    return moviese

@app.get('/movies/title/{title}',tags=['movies'])
def get_movie_by_title(title:str):
    moviese = list(filter(lambda x:x['title'] == title,var_movies))
    if len(moviese) == 0:
        return "title not found"
    return moviese

@app.get('/movies/',tags=['movies'])
def get_movie_all(title : str = "",category : str = "", year : str = "",rating : str = ""):
    global var_movies
    temp_var_movies = var_movies
    if title != "":
        return get_movie_by_title(title)
    else:
        dictionary_tool = {'category':category,'year':year,'rating':rating}
        for i in dictionary_tool:
            if dictionary_tool[i] != "": 
                temp_var_movies = var_movies
                view = list(filter(lambda x:x[i] == dictionary_tool[i], temp_var_movies))
                temp_var_movies = view 
            else:
                continue
    if len(temp_var_movies) == 0 or var_movies == temp_var_movies: 
        return "The Search is empty, please enter again..."
    return temp_var_movies 
        

@app.post('/movies',tags = ['movies'])
def create_movie(title:str = Body(),overview:str = Body(),year:str = Body(),rating:str = Body(), category:str =  Body()):
    new = {'id':len(var_movies)+1,'title':title,'overview':overview,'year':year,'rating':rating,'category':category}
    var_movies.append(new)
    return new['id']


@app.delete('/movie/{id}',tags=['movies'])
def delete_movie(id:int):
    return True
