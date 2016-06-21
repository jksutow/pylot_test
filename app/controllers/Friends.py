
from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)
        self.load_model('Friend')
        self.db = self._app.db

    def index(self):
        return self.load_view('loginreg.html')

    def register(self):
        print 'hello create'
        user_info = {
            'name': request.form['name'],
            'alias': request.form['alias'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_pw':request.form['confirm_pw'],
            'birthday': request.form['birthday']
        }
        create_user = self.models['Friend'].user_register(user_info)
        if create_user['status'] == True:
            session['id'] = create_user['user']['id']
            session['name'] = create_user['user']['name']
            session['alias'] = create_user['user']['alias']
            session['email'] = create_user['user']['email']
            session['password'] = create_user['user']['pw_hash']
            session['birthday'] = create_user['user']['birthday']

            return redirect('/profile')
        else:
            for message in create_user['errors']:
                flash(message, 'Errors are present.')
            return redirect('/')

    def login(self):
        login_info = {
            "email" : request.form['email'],
            "password" : request.form['password']
        }
        user_login = self.models['Friend'].login_user(login_info)
        if user_login['status'] == True:
            session['email'] = user_login['user']['email']
            session['id'] = user_login['user']['id']
            session['name'] = user_login['user']['name']
            return redirect('/profile')
        else:
            for message in user_login['errors']:
                flash(message,'errors')
            return redirect('/')

    # USER PROFILE PAGE DISPLAYING FRIENDS
    def user_home(self):
        id = session['id']
        friends = self.models['Friend'].get_all_friends_by_id(id)

        non_friends = self.models['Friend'].get_non_friends(id)
        # print "********", non_friends
        length = len(friends)
        return self.load_view('user_home.html', friends=friends, non_friends=non_friends, length=length)

    # VIEW FRIENDS PROFILE
    def view_friend_profile(self, id):
        friends = self.models['Friend'].get_friend_by_id(id)
        return self.load_view('friend_profile.html', friends=friends[0])

    #VIEW NON FRIEND PROFILE
    def view_non_friend(self, id):
        non_friends = self.models['Friend'].get_friend_by_id(id)
        return self.load_view('non_friend_profile.html', non_friends = non_friends[0])

    def add_friend(self, id):
        self.models['Friend'].add_friend(id, session['id'])
        return redirect('/profile')

    def delete(self, id):
        self.models['Friend'].delete_friend(id)
        return redirect('/profile')

    def logout(self):
        session.clear()
        return redirect('/')
