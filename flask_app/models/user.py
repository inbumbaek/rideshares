from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mydb = 'ohana'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(mydb).query_db(query)
        output = []
        for user_dictionary in results:
            output.append(cls(user_dictionary))
        return output

    @classmethod
    def save(cls, data):
        query ='''
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        '''
        user_id = connectToMySQL(mydb).query_db(query, data)
        # print(user_id)
        return user_id

    @classmethod
    def get_by_id(cls, data):
        query  = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(mydb).query_db(query, data)
        # print(results)
        this_user = cls(results[0])
        # print(this_user)
        return this_user

    @staticmethod
    def validate_user(request):
        is_valid = True
        if len(request["first_name"]) < 1:
            is_valid = False
            flash("First Name required.", "regError")
        elif len(request["first_name"]) < 2:
            is_valid = False
            flash("First Name Must Be Longer", "regError")
        if len(request["last_name"]) < 1:
            is_valid = False
            flash("Last Name required.", "regError")
        elif len(request["last_name"]) < 2:
            is_valid = False
            flash("Last Name Must Be Longer", "regError")
        if len(request["email"]) < 1:
            is_valid = False
            flash("Email Required.", "regError")
        elif not EMAIL_REGEX.match(request['email']):
            is_valid = False
            flash("Invalid Email", "regError")
        if len(request["password"]) < 1:
            is_valid = False
            flash("Password Required", "regError")
        elif request["password"] != request["passConf"]:
            is_valid = False
            flash("Passwords Much Match", "regError")
        if User.get_by_email(request):
            is_valid = False
            flash("Choose Another Email", "regError")
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(mydb).query_db(query,data)
        # print(result)
        if len(result) < 1:
            return False
        return cls(result[0])