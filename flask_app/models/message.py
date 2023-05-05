from flask_app.config.mysqlconnection import connectToMySQL
dateFormat = "%#m/%#d/%Y %I:%M %p"
from flask_app.models import user
mydb = 'ohana'

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ride_id = data['ride_id']
        self.user_id = data['user_id']
        self.sender = None

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO messages (content, ride_id, user_id)
        VALUES(%(content)s, %(ride_id)s, %(user_id)s);
        '''
        return connectToMySQL(mydb).query_db(query, data)
    
    @classmethod
    def get_all_join_user(cls, data):
        query = '''
        SELECT *
        FROM messages
        JOIN users
        ON messages.user_id = users.id
        WHERE messages.ride_id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        output = []
        for row in results:
            this_message = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            this_message.sender = user.User(user_data)
            # add rides to my output list
            output.append(this_message)
        return output