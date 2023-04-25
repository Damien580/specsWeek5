#this file will erase old db, create new db, and seed info into new db.

import os
import json 
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings") #deletes old database
os.system("createdb ratings") #creates new database

model.connect_to_db(server.app) #connects to server

with server.app.app_context():#wraps ebverything below in the app.app_contect

    model.db.create_all() #creates all new empty tables
    
    with open('data/movies.json') as f: #this function reads the data from the json file 'movies',
        movie_data = json.loads(f.read()) #and makes a list of dictionaries
        
    movies_in_db = []
    
    for movie in movie_data: #this loops over list of dictionaries.
        title, overview, poster_path = (movie["title"], movie["overview"], movie["poster_path"]) #grabs movie info from dictionaries in the list 'movie_data'.
        release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d") #this creates the date time function and formats the display.
        
        db_movie = crud.create_movie(title, overview, release_date, poster_path) #uses the create_movie func to fill in the db_movie variablefor all movies in the json file
        movies_in_db.append(db_movie) #appends db_movie to the movies_in_db list, for all movies in the json file
    
    model.db.session.add_all(movies_in_db) #this adds all movie data to the table.
    model.db.session.commit() #this commits the changes that have been made. nothing is saved if this is not run.
    
    for n in range(10):
        email = f'user{n}@test.com'
        password = 'test'
        
        user = crud.create_user(email, password)
        model.db.session.add(user)
        
        for _ in range(10):
            random_movie=choice(movies_in_db)
            score = randint(1, 5)
            
            rating = crud.create_rating(user, random_movie, score)
            model.db.session.add(rating)
            
    model.db.session.commit()