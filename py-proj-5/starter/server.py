"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/") #route to view homepage
def homepage():
    return render_template("homepage.html")

@app.route("/movies") #route to view all movies page
def all_movies():
    movies = crud.get_movies() #gets movies and assigns them to a variable
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>") #route to display a movies info
def show_movie(movie_id): #func to get movie details
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    users = crud.get_users()
    return render_template("/all_users.html", users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/users/<user_id>")
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route("/login", methods=["POST"])
def process_login():
    
    email = request.form.get("email") #gets email info from inputs on home page
    password = request.form.get("password")
    
    user= crud.get_user_by_email(email) #finds user by email
    if not user or user.password != password: #if email is not registered or password doesnt match flash message telling user to try again
        flash("The email or password you entered is incorrect. Please try again.")
    else:
        session["user_email"] = user.email #this logs in user by storing users email to session    
        flash(f"Welcome back, {user.email}!")
    return redirect("/")

@app.route("/logout") #endpoint for logout page
def logout(): #function to log out
    logged_in_email = session.get("user_email")
    
    if logged_in_email == ("user_email"):
        del session["user_email"] #deletes session token for the user
        flash("logged Out!")
        return redirect("/")
    else:
        flash("You are not logged in!")
        return redirect("/")


@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", debug=True, port=8000)
