from system.core.model import Model
#import for email regex
import re
# regex for email
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class Friend(Model):
    def __init__(self):
        super(Friend, self).__init__()

    def user_register(self, info):
        errors = []

        if not info['name']:
            errors.append('Name cannot be blank')

        if not info['alias']:
            errors.append('Alias cannot be blank')

        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid')

        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match')

        if not info['birthday']:
            errors.append('Birthday cannot be blank')

        if errors:
            return {
                "status": False,
                "errors": errors
            }

        else:
            password = info['password']
            pw_hash = self.bcrypt.generate_password_hash(password)
            query = 'INSERT INTO users (name, alias, email, pw_hash, birthday, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, :birthday, NOW(), NOW())'
            data={
                'name': info['name'],
                'alias': info['alias'],
                'email': info['email'],
                'pw_hash': pw_hash,
                'birthday': info['birthday']
            }
            self.db.query_db(query, data)

            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)

            return {
                "status": True,
                "user": users[0]
            }

    def login_user(self, login_info):
        errors = []

        if not login_info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(login_info['email']):
            errors.append('Please enter a valid email address')

        if not login_info['password']:
            errors.append('Password cannot be blank')
        if errors:
            return {
                'status': False,
                'errors': errors
            }
        else:
            password = login_info['password']
            user_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(login_info['email'])
            users = self.db.query_db(user_query)

            if users[0]:
                if self.bcrypt.check_password_hash(users[0]['pw_hash'], password):
                    return {
                        "status": True,
                        "user": users[0]
                    }
                else:
                    errors.append('Incorrect password')
                    return {
                        'status': False,
                        'errors': errors
                    }
    def get_all_friends_by_id(self, id):
        query = "SELECT users.alias as user_name, users2.alias as friend_name, friends.friends_id as friend_id FROM users LEFT JOIN friends ON users.id = friends.user_id LEFT JOIN users as users2 ON users2.id = friends.friends_id WHERE friends.user_id = '{}'".format(id)

        friends = self.db.query_db(query)
        return friends

    def get_non_friends(self, id):
        query = "SELECT id, name, alias, email, birthday FROM users WHERE id != '{}'".format(id)

        non_friends = self.db.query_db(query)
        return non_friends


    def get_friend_by_id(self, id):
        query = "SELECT * FROM users WHERE id = '{}'".format(id)
        return self.db.query_db(query)

    def add_friend(self, id, user_id):
        query = "INSERT INTO friends(user_id, friends_id, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(user_id, id)

        return self.db.query_db(query)

    def delete_friend(self, id):
        query = "DELETE FROM friends WHERE friends_id='{}'".format(id)
        return self.db.query_db(query)
