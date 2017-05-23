from flask import Flask, make_response, abort, jsonify, url_for, request
from flask_httpauth import HTTPBasicAuth
import time

auth = HTTPBasicAuth()

app = Flask(__name__)

app.config.update({
    "DEBUG": True
})

users = [
    {
        'username': 'nitin',
        'age': 21,
        'city': 'Delhi',
        'password': 'gupta',
        'bio': 'confused person in the world'
    },
    {
        'username': 'shivam',
        'age': 20,
        'city': 'Delhi',
        'password': 'monga',
        'bio': 'person who loves challenges'
    },
    {
        'username': 'dhannu',
        'age': 23,
        'city': 'Delhi',
        'password': 'mayank',
        'bio': 'married person'
    }
]

places = [
    {
        'placename': 'Sarita vihar',
        'text': 'a good place to live',
        'likes': 10,
        'comments': 12,
        'username': 'nitin',
        'id': 1,
        'addedOn': time.strftime('%d/%m/%Y')

    },
    {
        'placename': 'Sarita vihar',
        'text': 'a place where you get all the things',
        'likes': 10,
        'comments': 12,
        'username': 'dhannu',
        'id': 1,
        'addedOn': time.strftime('%d/%m/%Y')

    },
    {
        'placename': 'Sultan Puri',
        'text': 'Mybirth place',
        'likes': 50,
        'comments': 100,
        'username': 'nitin',
        'id': 2,
        'addedOn': time.strftime('%d/%m/%Y')
    }
]

comments = [
    {
        'username': 'nitin',
        'id': 1,
        'addedOn': time.strftime('%d/%m/%Y'),
        'comment': "lovely place to stay"
    },
    {
        'username': 'nitin',
        'id': 2,
        'addedOn': time.strftime('%d/%m/%Y'),
        'comment': 'the first place i visit'
    },
    {
        'username': 'dhannu',
        'id': 2,
        'addedOn': time.strftime('%d/%m/%Y'),
        'comment': 'the first place i visit'
    }


]


@app.route('/user', methods=['POST'])
def new_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user = {
        'name': request.json['username'],
        'password': request.json['password'],
        'age': request.json['age'],
        'city': request.json['city'],
        'bio': request.json['bio']
    }
    users.append(user)
    return jsonify({'user': user}), 201


@app.route('/places', methods=['POST'])
def add_place():
    if not request.json or not 'placename' in request.json:
        abort(400)
    place = {
        'placename': request.json['placename'],
        'text': request.json['text'],
        'likes': places[-1]['likes'] + 1,
        'comments': places[-1]['comments'] + 1,
        'usename': auth.username(),
        'addedOn': time.strftime('%d/%m/%Y')
    }
    places.append(place)
    return jsonify({'place': place})


@auth.get_password
def get_password(username):
    user = [user for user in users if username == user['username']]
    if len(user) == 0:
        abort(400)
    return user[0]['password']


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized'}), 401)


@app.route('/getuser', methods=['GET'])
@auth.login_required
def get_user():
    user = [user for user in users if auth.username() == user['username']]
    return jsonify({'user': user})


@app.route('/getplaces', methods=['GET'])
@auth.login_required
def get_places():
    place = [place for place in places if auth.username() == place['username']]
    return jsonify({'users': place})


@app.route('/getuser/particular_place/<int:place_id>', methods=['GET'])
@auth.login_required
def get_current_place(place_id):
    place = [place for place in places if auth.username() == place['username']]
    one_place = [one_place for one_place in places if place_id == one_place['id']]
    return jsonify({'user_place': one_place}), 201


@app.route('/getuser/info', methods=['GET'])
@auth.login_required
def get_users():
    find = [place for place in places if auth.username() == place['username']]
    return jsonify({'places': find})

@app.route('/put/user/update_place/<int:place_id>', methods=['PUT'])
@auth.login_required
def update_place_from_id(place_id):
   all_user_place =[all_user_place for all_user_place in places if auth.username() ==all_user_place['username']]
   id_place =[id_place for id_place in all_user_place if place_id ==id_place['id']]
   if len(id_place) == 0:
      abort(404)
   if not request.json:
      abort(400)
   if 'text' in request.json and type(request.json['text']) is not unicode:
      abort(400)
   # if 'likes' in request.json and type(request.json['likess']) is not unicode:
   #    abort(400)
   id_place[0]['text'] = request.json.get('text', id_place[0]['text'])
   # id_place[0]['likes'] =request.json.get('likes', id_place[0]['likes'])

   return jsonify({'update_place': id_place[0]})


@app.route('/get/comment_from_id/<int:comment_id>', methods = ['GET'])
@auth.login_required
def comment_from_id(comment_id):
    user_comment = [user_comment for user_comment in comments if auth.username()==user_comment['username']]
    one_comment = [one_comment for one_comment in user_comment if comment_id == one_comment['id']]
    return jsonify({'user_place':one_comment}),201

@app.route('/add_comment/<int:comment_id>', methods = ['POST'])
@auth.login_required
def add_comment(comment_id):
    comment = [comment for comment in comments if comment_id==comment['id']]
    particular_comment = [particular_comment for particular_comment in comment if auth.username()==particular_comment['username']]
    if not request.json or not 'comment' in request.json:
        abort(400)
    add = {
        'username': auth.username(),
        'addedOn': time.strftime('%d/%m/%Y'),
        'comment':request.json['comment']
    }
    comments.append(add)
    return jsonify({'comment':add})





if __name__ == "__main__":
    app.run()
