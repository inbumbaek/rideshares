from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
mydb = 'ohana'

class Ride:
    def __init__(self,data):
        self.id = data['id']
        self.destination = data['destination']
        self.pick_up = data['pick_up']
        self.ride_date = data['ride_date']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.passenger_id = data['passenger_id']
        self.driver_id = data['driver_id']
        self.passenger = None

    @classmethod
    def get_all_with_no_driver(cls):
        query = '''
        SELECT *
        FROM rides
        JOIN users
        ON rides.passenger_id = users.id
        WHERE rides.driver_id IS NULL;'''
        results = connectToMySQL(mydb).query_db(query)
        # print(results)
        output = []
        # loop through results
        for row in results:
            # print(row)
            # create ride objects
            this_ride = cls(row)
            # create passenger user objects
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            user_passenger = user.User(user_data)
            # set the ride.passenger = passenger user objects
            this_ride.passenger = user_passenger
            # add rides to my output list
            output.append(this_ride)
            # return that list
        return output
    
    @classmethod
    def get_all_with_driver(cls):
        query = '''
        SELECT * 
        FROM rides R
        JOIN users UP
        ON UP.id = R.passenger_id
        JOIN users UD
        ON UD.id = R.driver_id;
        '''
        results = connectToMySQL(mydb).query_db(query)
        # print(results)
        output = []
        # loop through results
        for row in results:
            # print(row)
            # create ride objects
            this_ride = cls(row)
            # create passenger user objects
            pass_data = {
                'id' : row['UP.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['UP.created_at'],
                'updated_at' : row['UP.updated_at']
            }
            user_passenger = user.User(pass_data)
            # set the ride.passenger = passenger user objects
            this_ride.passenger = user_passenger
            drive_data = {
                'id' : row['UD.id'],
                'first_name' : row['UD.first_name'],
                'last_name' : row['UD.last_name'],
                'email' : row['UD.email'],
                'password' : row['UD.password'],
                'created_at' : row['UD.created_at'],
                'updated_at' : row['UD.updated_at']
            }
            user_driver = user.User(drive_data)
            this_ride.driver = user_driver
            # add rides to my output list
            output.append(this_ride)
            # return that list
        return output

    @classmethod
    def save(cls, data):
        query ='''
        INSERT INTO rides (destination, pick_up, ride_date, details, passenger_id) 
        VALUES(%(destination)s, %(pick_up)s, %(ride_date)s, %(details)s, %(passenger_id)s);
        '''
        ride_id = connectToMySQL(mydb).query_db(query, data)
        # print(ride_id)
        return ride_id

    @staticmethod
    def validate_ride(request):
        is_valid = True
        if len(request["destination"]) < 1:
            is_valid = False
            flash("destination required")
        elif len(request["destination"]) <= 2:
            is_valid = False
            flash("destination Must Be Longer")
        if len(request["pick_up"]) < 1:
            is_valid = False
            flash("pick_up required.")
        elif len(request["pick_up"]) <= 2:
            is_valid = False
            flash("pick up Must Be Longer")
        if len(request["ride_date"]) < 1:
            is_valid = False
            flash("DateRequired.")
        if len(request["details"]) < 1:
            is_valid = False
            flash("details Required")
        elif len(request["details"]) <= 9:
            is_valid = False
            flash("details Must Be Longer")
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = '''
        DELETE FROM rides
        WHERE id = %(id)s;
        '''
        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def add_driver(cls, data):
        query = '''
        UPDATE rides
        SET driver_id = %(driver_id)s
        WHERE id = %(id)s
        '''
        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def remove_driver(cls, ride_id):
        data = {
            'id' : ride_id,
            'driver_id' : None
        }
        query = '''
        UPDATE rides
        SET driver_id = %(driver_id)s
        WHERE id = %(id)s
        '''
        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = '''
        SELECT * 
        FROM rides R
        JOIN users UP
        ON UP.id = R.passenger_id
        JOIN users UD
        ON UD.id = R.driver_id
        WHERE R.id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        # print(results)
        this_ride = cls(results[0])
        # loop through results
        for row in results:
            # print(row)
            # create ride objects
            # this_ride = cls(row)
            # create passenger user objects
            pass_data = {
                'id' : row['UP.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['UP.created_at'],
                'updated_at' : row['UP.updated_at']
            }
            user_passenger = user.User(pass_data)
            # set the ride.passenger = passenger user objects
            this_ride.passenger = user_passenger
            drive_data = {
                'id' : row['UD.id'],
                'first_name' : row['UD.first_name'],
                'last_name' : row['UD.last_name'],
                'email' : row['UD.email'],
                'password' : row['UD.password'],
                'created_at' : row['UD.created_at'],
                'updated_at' : row['UD.updated_at']
            }
            user_driver = user.User(drive_data)
            this_ride.driver = user_driver
            # return that list
        return this_ride

    @classmethod 
    def update(cls,data):
        query = '''
        UPDATE rides 
        SET pick_up=%(pick_up)s,details=%(details)s 
        WHERE id = %(id)s'''
        connectToMySQL(mydb).query_db(query,data)