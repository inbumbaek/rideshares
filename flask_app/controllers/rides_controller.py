from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import ride, message
dateFormat = "%#m/%#d/%Y %I:%M %p"

@app.route('/ride/new')
def add_ride():
    if 'user_id' in session:
        return render_template('create.html')
    return redirect('/')

@app.route('/ride/create', methods=['post'])
def create_ride():
    if 'user_id' in session:
        # print(request.form)
        # validate ride info
        if ride.Ride.validate_ride(request.form):
            pass
            # save ride info
            # data = request.form.to_dict()
            # data['passenger_id'] = session['user_id']
            data = {
                'destination' : request.form['destination'],
                'pick_up' : request.form['pick_up'],
                'ride_date' : request.form['ride_date'],
                'passenger_id' : session['user_id'],
                'details' : request.form['details']
            }
            # print(data)
            ride.Ride.save(data)
            return redirect('/landing')
        return redirect('/ride/new')
    return redirect('/')

@app.route('/ride/delete/<int:ride_id>')
def delete_ride(ride_id):
    if 'user_id' in session:
        # call delete class method
        ride.Ride.delete({'id':ride_id})
        # redirect to dashboard?
        return redirect('/landing')
    return redirect('/')

@app.route('/ride/drive/<int:ride_id>')
def add_driver(ride_id):
    if 'user_id' in session:
    # create classmethod to add driver id to ride object
        data = {
            'id' : ride_id,
            'driver_id' : session['user_id']
        }
        ride.Ride.add_driver(data)
        return redirect('/landing')
    return redirect('/')

@app.route('/ride/cancel/<int:ride_id>')
def remove_driver(ride_id):
    if 'user_id' in session:
    # create classmethod to remove driver id from ride object
        ride.Ride.remove_driver(ride_id)
        return redirect('/landing')
    return redirect('/')

@app.route('/ride/show/<int:ride_id>')
def show_ride(ride_id):
    if 'user_id' in session:
        return render_template('show.html',
            ride = ride.Ride.get_by_id({'id': ride_id}),
            ride_messages = message.Message.get_all_join_user({'id':ride_id}))
    return redirect('/')

@app.route('/ride/update/<int:ride_id>', methods=['POST'])
def update(ride_id):
    print(request.form)
    if 'user_id' in session:
        ride.Ride.update({
            'id':ride_id,
            'pick_up': request.form['pick_up'],
            'details': request.form['details']
        })
        return redirect('/landing')
    return redirect('/')

@app.route('/ride/edit/<int:ride_id>')
def edit(ride_id):
    return render_template("update.html",ride = ride.Ride.get_by_id({"id": ride_id}))