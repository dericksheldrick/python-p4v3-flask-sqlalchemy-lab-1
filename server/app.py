# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        data ={
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year" : earthquake.year
        }
        response = make_response(data, 200)
    else:
        error_message = {"message":f'Earthquake {id} not found.'}
        response = make_response(error_message, 404)
    
    return response

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    list = [{
        "id":quake.id,
        "location": quake.location,
        "magnitude": quake.magnitude,
        "year": quake.year

    } for quake in earthquakes]

    response = {
        "count":len(list),
        "quakes": list
    }

    return make_response(response, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
