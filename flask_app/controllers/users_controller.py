from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, ride, message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
dateFormat = "%#m/%#d/%Y %I:%M %p"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods =['POST'])
def reg():
    if user.User.validate_user(request.form):
        hashed_pass = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : hashed_pass
        }
        user_id = user.User.save(data)
        session["user_id"] = user_id
        return redirect('/landing')
    flash("Invalid Email", 'regError')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    this_user = user.User.get_by_email(request.form)
    # print(this_user)
    if this_user:
        if bcrypt.check_password_hash(this_user.password, request.form['password']):
            session["user_id"] = this_user.id
            return redirect('/landing')
    flash("Invalid Credentials", 'logError')
    return redirect('/')

@app.route('/landing')
def landing():
    if 'user_id' in session:
        return render_template('dashboard.html', 
            user = user.User.get_by_id({'id': session['user_id']}),
            requests = ride.Ride.get_all_with_no_driver(),
            booked = ride.Ride.get_all_with_driver())
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/message/create/<int:ride_id>', methods = ['POST'])
def create_message(ride_id):
    if 'user_id' in session:
        # sng the session id
        # add the ids to the request .form
        data = request.form.to_dict()
        data['ride_id'] = ride_id
        data['user_id'] = session['user_id']
        # call the class to create a message
        message.Message.save(data)
        return redirect(f'/ride/show/{ride_id}')
    return redirect('/')