#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route( '/campers', methods=[ "GET", "POST" ] )
def campers():
    if request.method == "GET":
        campers = [ c_to_dict( camper ) for camper in Camper.query.all() ]
        return make_response( jsonify( campers ), 200 )
    
    elif request.method == "POST":
        new_c = Camper(
            name = request.get_json()[ 'name' ],
            age = request.get_json()[ 'age' ]
        )
        db.session.add( new_c )
        db.session.commit()

        return make_response( jsonify( c_to_dict( new_c )), 201 )

@app.route( '/campers/<int:id>', methods=[ "GET" ] )
def camper( id ):

    if request.method == "GET":
        camper = Camper.query.filter_by( id=id ).first()
        return make_response( jsonify( c_to_dict( camper )), 200 )

@app.route( '/activities', methods=[ "GET" ] )
def activities():
    if request.method == "GET":
        activities = [ a_to_dict( activity ) for activity in Activity.query.all() ]
        return make_response( jsonify( activities ), 200 )
    
@app.route( '/activities/<int:id>', methods=[ "DELETE" ] )
def activity( id ):
    activity = Activity.query.filter_by( id=id ).first()
    if activity:
        db.session.delete( activity )
        db.session.commit()
        return make_response( jsonify( '', 404 ) )
    else:
        return make_response( jsonify( "Activity not found.", 404) )
    
@app.route( '/signups', methods=[ "POST" ] )
def signups():
    if request.method == "POST":
        new_s = Signup(
            time = request.get_json()[ 'time' ],
            camper_id = request.get_json()[ 'camper_id' ],
            activity_id = request.get_json()[ 'activity_id' ]
        )
        db.session.add( new_s )
        db.session.commit()

        camper = Camper.query.filter_by( id = request.get_json()[ 'camper_id' ]).first()
        activity = Activity.query.filter_by( id = request.get_json()[ 'activity_id' ]).first()

        response = {
            "activity": a_to_dict( activity )
        }

        return make_response( jsonify( response ), 201 )

def c_to_dict( c ):
    return {
        "id": c.id,
        "name": c.name,
        "age": c.age
    }

def a_to_dict( a ):
    return {
        "id": a.id,
        "name": a.name,
        "difficulty": a.difficulty
    }

def s_to_dict( s ):
    return {
        "id": s.id,
        "time": s.time,
        "camper_id": s.camper_id,
        "activity_id": s.activity_id
    }


if __name__ == '__main__':
    app.run(port=5555, debug=True)























# #!/usr/bin/env python3

# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

# from flask import Flask, make_response, jsonify, request
# from flask_migrate import Migrate
# from flask_restful import Api, Resource

# from models import db, Activity, Camper, Signup

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/')
# def home():
#     return ''

# @app.route( '/campers', methods=[ "GET", "POST" ] )
# def campers():

#     if request.method == "GET":
#         campers = [ c_to_dict( camper ) for camper in Camper.query.all() ]
#         return make_response( jsonify( campers), 200 )
    
#     elif request.method == "POST":
#         new_c = Camper(
#             name = request.get_json()[ 'name' ],
#             age = request.get_json()[ 'age' ]
#         )
#         db.session.add( new_c )
#         db.session.commit()

#         return make_response( jsonify( c_to_dict( new_c )), 201 )

# @app.route( '/campers/<int:id>', methods=[ "GET" ] )
# def camper( id ):
#     camper = Camper.query.filter( Camper.id == id ).first()
#     return make_response( jsonify( c_to_dict( camper )), 200 )

# @app.route( '/activities', methods=[ "GET" ] )
# def activities():
#     activities = [ a_to_dict( activity ) for activity in Activity.query.all() ]
#     return make_response( jsonify( activities ), 200 )

# @app.route( '/activities/<int:id>', methods=[ "DELETE" ] )
# def activity( id ):
#     activity = Activity.query.filter_by( id = id ).first()
#     if activity:
#         db.session.delete( activity )
#         db.session.commit()
#         return make_response( jsonify( '', 404 ) )
#     else: 
#         return make_response( jsonify( "Activity not found.", 404 ))

# @app.route( '/signups', methods=[ "POST" ] )
# def signup():
#     if request.method == "POST":
#         new_s = Signup(
#             time = request.get_json()[ 'time' ],
#             camper_id = request.get_json()[ 'camper_id' ],
#             activity_id = request.get_json()[ 'activity_id' ]
#         )
#         db.session.add( new_s )
#         db.session.commit()

#         return make_response( jsonify( s_to_dict( new_s )), 201 )

# def c_to_dict( camper ):
#     return {
#         "id": camper.id,
#         "name": camper.name,
#         "age": camper.age
#     }

# def a_to_dict( activity ):
#     return {
#         "id": activity.id,
#         "name": activity.name,
#         "difficulty": activity.difficulty
#     }

# def s_to_dict( signup ):
#     return {
#         "id": signup.id,
#         "time": signup.time,
#         "camper_id": signup.camper_id,
#         "activity_id": signup.activity_id
#     }

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)
