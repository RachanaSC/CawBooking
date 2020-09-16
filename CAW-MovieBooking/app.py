from flask import Flask, render_template, request, session, url_for, redirect
from models.booking import Booking
from models.movie import Movie
from models.user import User
from models.screen import Screen

app = Flask(__name__)
app.secret_key ="Rachana"

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.route('/logout')
def logout_template():
    session['email'] = None
    return redirect(url_for('home_template'))

@app.route('/profile')
def profile_template():
    print(session['email'])
    if session['email'] is not None:
        print(session['email'])
        user = User.get_by_email(session['email'])
        username=user.name
        bookings = user.get_bookings()
        return render_template("profile.html",bookings=bookings,email=user.email,name=username)
    else:
        return redirect(url_for('login_template'))

@app.route('/')
def home_template():
    movies = Movie.all()
    #print(movies)
    return render_template("index.html", movies=movies)

@app.route('/city/<string:city>')
def city_template(city):
    screens = Screen.get_by_city(city)
    movies = {}
    for screen in screens:
        movie = Movie.get_by_id(screen.movie_id)
        movies[screen._id] = {"name": movie.name, "description": movie.description}
    return render_template("city.html", movies=movies ,city=city ,screens=screens)

@app.route('/allscreen')
def allscreen_template():
    screens = Screen.all()
    movies = {}
    for screen in screens:
        movie = Movie.get_by_id(screen.movie_id)
        movies[screen._id] = {"name" :movie.name , "description":movie.description}
    #print(movies)
    return render_template("allscreen.html", screens=screens,movies=movies)

@app.route('/auth/login' , methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
        return redirect(url_for('profile_template'))
    else:
        session['email'] = None
        return render_template("login.html", error="Invalid Login!")

@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    User.register(name, email, password)
    return render_template("profile.html", email=session['email'] )

@app.route('/booking/<string:screen_id>',methods =['POST', 'GET'])
def make_booking(screen_id):
    if session['email'] is not None:
        user = User.get_by_email(session['email'])
        if request.method == 'GET':
            screen = Screen.get_by_id(screen_id)
            movie = Movie.get_by_id(screen.movie_id)
            ava_seats = int(screen.total_seats) - int(screen.booked_seats)
            return render_template("booking.html", screen=screen , movie = movie ,ava_seats=ava_seats)
        else:
                screen = Screen.get_by_id(screen_id)
                movie = Movie.get_by_id(screen.movie_id)
                no_of_seats = request.form['seats']
                updateseats = int(screen.booked_seats) + int(no_of_seats)
                screen.update_seats(screen._id,updateseats) #update seat count
                total_price = int(screen.price) * int(no_of_seats)
                booking = Booking(user._id ,screen._id,screen.movie_id,movie.name,no_of_seats,total_price)
                booking.save_to_mongo()
                return redirect(url_for('profile_template'))

    else:
            return redirect(url_for('login_template'))

if __name__=='__main__':
    app.run()
    #app.run(port=4995)