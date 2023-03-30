
from fastapi import Depends,FastAPI, Path, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

class JWTBearer(HTTPBearer):
    async def __call__(self, request : Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code = 403,detail = "Credenciales son invalidas")

class User(BaseModel):
    email : str
    password : str

class Movie(BaseModel):
    id : Optional[int] 
    title : str 
    overview : str
    year : str
    rating : str = None
    category : str

    class Config:
        schema_extra = {
            'example':{
                'id' : 'Automatic Generation',
                'title' : 'Title of movie',
                'overview' : 'Some about the theme or plot of movie',
                'year' : 'movie release year',
                'rating' : 'Depend of views',
                'category' : 'Category of movie, Action, Adventure, ...'
            }
        }


    @validator('title')
    def title_check(cls,title):
        long = len(title)
        if long < 4:
            return ValueError(f"The title must have minumum 4 characters, actual characters : {long}")
        elif long > 30:
            return ValueError(f"The title must have maximum 30 characters, actual characters {long}")
        return title
    
    @validator('year')
    def year_check(cls,year):
        actual_year = int(datetime.now().strftime("%Y"))
        oldest_year = 1888
        if int(year) > actual_year:
            return Exception(f"The year of movie can't be more than actual year, entered year {year}")
        elif int(year) < oldest_year:
            return Exception(f"The year of movie can't be less than actual year, entered year {year}")
        return year
    
    @validator('id')
    def id_for_Movie(cls,id):
        id = len(var_movies) + 1
        var_movies.append(id)
        return id
    
    @validator('category')
    def check_category(cls,category):
        categories = ['Accion','Terror','Drama','Comedia','Romance','Documental','Infantil','Anime',
                      'Thriller','Suspenso','History of life','Aventura']
        if category not in categories:
            raise Exception(f'{category} is not a possible category, please enter again')
        return category
    
    @validator('overview')
    def check_overview(cls,overview):
        long = len(overview)
        if long < 15:
            raise Exception(f'Overview must have minimum 15 characters of lenght, now : {long}')
        elif long > 200:
            raise Exception(f'Overview must have maximum 200 characters of lenght, now : {long}')
        return overview
        

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
    "overview": "Nino de madera que tiene un ada madrina y por desobediente se sale de la casa",
    "year": "2000",
    "rating": "8.8",
    "category": "Aventura" 
    },
    {
    "id":3,
    "title":"Enredados",
    "overview": "princesa robada por sus poderes curativos que vive en una torre alejada de toda civilizacion, pero un princesa o tal vez un ladron ira en su rescate",
    "year": "2010",
    "rating": "8.2",
    "category": "Aventura" 
    },
    {
    "id":4,
    "title":"The last of us",
    "overview": "El mundo ha caido ante un plaga mortal, el cordiceps, pero nuestro heroe joel descububre esperanzas junto con la pequeña eli",
    "year": "2020",
    "rating": "9.4",
    "category": "Accion" 
    },
    {
    "id":5,
    "title":"Queen",
    "overview": "Histografia de la famosa banda queen, peleas, records y amores",
    "year": "2019",
    "rating": "10",
    "category": "Drama" 
    },
    {
    "id":6,
    "title":"Internal Robot",
    "overview": "Un hacker trata de destruir el sistema de seguridad de la milicia estado unidense, pero no se espera que muchos como el harán hasta lo imposible para que lo logre",
    "year": "2008",
    "rating": "7.5",
    "category": "Accion" 
    },
    {
    "id":7,
    "title":"Mario Bros",
    "overview": "Un particular fontanero ha vuelto a ciudad champiñon, pero no se espera lo que sucederá, caos, una princesa perdida, y una tripulación de tortugas",
    "year": "2002",
    "rating": "9.1",
    "category": "Aventura" 
    },
    {
    "id":8,
    "title":"STOLEN LIFE",
    "overview": "Cuenta la historia de un tribunal donde el abogado mike tendra que elegir entre sus principios morales y su estatus como mejor abogado de toda la zona",
    "year": "2004",
    "rating": "10",
    "category": "Drama" 
    },
    {
    "id":9,
    "title":"Historias fantasmas",
    "overview": "Nos relata en una pelicula/documental las historias de los ancestros indigenas que vivian en el sur colombiano",
    "year": "2022",
    "rating": "8.9",
    "category": "Drama" 
    },
    {
    "id":10,
    "title":"The pop's king",
    "overview": "Relata la historia del famoso artista Michael Jackson",
    "year": "2023",
    "rating": "7.9",
    "category": "Drama" 
    }
]

@app.get("/",tags = ['home'],response_class = HTMLResponse)
def message():
    return HTMLResponse('<h1>Welcome to Movie Practice API :D</h1>')

@app.post('/login',tags=['auth'])
def login(user : User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token : str = create_token(user.dict())
    return JSONResponse(status_code = 200, content = token)

@app.get('/movies',tags = ['movies'], response_model=List[Movie],status_code=200,dependencies = [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code = 200,content = var_movies)

@app.get('/movies/{id}',tags=['movies'], response_model = Movie,status_code=200)
def get_movie(id : int = Path(ge=1, le=len(var_movies))) -> Movie:
    movie = list(filter(lambda x:x['id']==id,var_movies))
    if len(movie) == 0:
        return JSONResponse(status_code = 404,content=[])
    return JSONResponse(status_code = 200,content = movie)

@app.get('/movies/title/{title}',tags=['movies'],response_model = Movie,status_code = 200)
def get_movie_by_title(title:str = Path(min_length=4, max_length=30)) -> Movie:
    moviese = list(filter(lambda x:x['title'] == title,var_movies))
    if len(moviese) == 0:
        return JSONResponse(status_code = 404,content = [])
    return JSONResponse(status_code = 200,content = moviese)

@app.get('/movies/',tags=['movies'], response_model = List[Movie],status_code=200)
def get_movie_all(category : str = "",year : str = "",rating : str = "", 
                  year_more : bool = False,
                  year_low : bool = False,rat_more : bool = False, 
                  rat_low : bool = False) -> List[Movie]:
##### ^^^ Parameters and variables of function ^^^ ################################################################
    global var_movies
    year_parameter = {'more':year_more,'low':year_low}
    rating_parameter = {'more':rat_more,'low':rat_low}
#### ^^^ Inicializating variables necesary to the rest or the process ^^^ #########################################
    if (year_low == True and year_more == True) or (rat_low == True and rat_more == True):
        return f'No possible filter of search, only you can select one, more than or low than'
    temp_var_movies = var_movies
#### ^^^ Value to override and parameter's validation of search about filters of year and rating ^^^ ###############
    dictionary_tool = {'category':[category,{'only':True}],'year':[year,year_parameter],'rating':[rating,rating_parameter]}
    for i in dictionary_tool:
        if dictionary_tool[i][0] != "" and len(dictionary_tool[i][1]) > 1: 
            if dictionary_tool[i][1]['more'] == True: 
                view = list(filter(lambda x:float(x[i]) >= float(dictionary_tool[i][0]), temp_var_movies))
            elif dictionary_tool[i][1]['low'] == True:
                view = list(filter(lambda x:float(x[i]) <= float(dictionary_tool[i][0]), temp_var_movies))
            else:
                view = list(filter(lambda x:float(x[i]) == float(dictionary_tool[i][0]), temp_var_movies)) 
            temp_var_movies = view 
        elif dictionary_tool[i][0] != "" and dictionary_tool[i][1]['only'] == True:
            view = list(filter(lambda x:x[i] == dictionary_tool[i][0], temp_var_movies))
            temp_var_movies = view 
#### ^^^ Algorithm proccess for the search ^^^ #####################################################################
    if len(temp_var_movies) == 0 or var_movies == temp_var_movies: 
        return JSONResponse(status_code = 404,content = [])
#### ^^^ Validation for results of search and default parameters entry for function ^^^ ############################
    return JSONResponse(status_code = 200,content = temp_var_movies) 
        
@app.post('/movies',tags = ['movies'], response_model = dict, status_code=201)
def create_movie(movie : Movie) -> dict:
    global var_movies
    movie.id = len(var_movies) + 1
    var_movies.append(movie.dict())
    return JSONResponse(status_code = 201,content = {'message':'The movie was add successfully'})


@app.delete('/movie/{id}',tags=['movies'],response_model = dict,status_code=200)
def delete_movie(id:int) -> dict:
    global var_movies
    counter = 0
    for movie in var_movies:
        counter += 1
        if movie['id']== id:
            var_movies.remove(movie)
            return JSONResponse(status_code = 200,content = {'message':'The movie was remove successfully'})
    return JSONResponse(status_code = 404,content = {'message':'The movie was not found'})

@app.put('/movie/{id}',tags=['movies'],response_model = dict,status_code=200)
def update_movie(id : int,movie : Movie) -> dict:
    global var_movies
    counter_parameter = 0
    for i in var_movies:
        if i['id'] == id:
            counter_parameter += 1
            i['title'] = movie.title 
            i['overview'] = movie.overview 
            i['year'] = movie.year
            i['rating'] = movie.rating
            i['category'] = movie.category
            return JSONResponse(status_code = 200,content = {'message':'The movie was update successfully'})
    return JSONResponse(status_code = 404,content = {'message':'The movie was not found'})

# This is no the main branch, just for see that