"""Models for movie ratings app."""

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
        # ratings = a list of Rating objects
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def __repr__(self):
        return f"<User id={self.user_id} email={self.email}>" 
    
class Movie(db.Model):
    __tablename__ = "movies"
    
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)
    
        # ratings = a list of Rating objects


    def __repr__(self):
        return f"<Movie movie_id={self.movie_id}, title={self.title}>"
    
    
class Rating(db.Model):
    __tablename__ = "ratings"
    
    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    
    movie = db.relationship("Movie", backref="ratings")
    user = db.relationship("User", backref="ratings")
    
    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score}>"




def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
