#!/usr/bin/python3
"""Script that starts a Flask web application:
    - web application must be listening on 0.0.0.0, port 5000
    - Routes:
        - /hbhb: display a HTML page: (inside the tag BODY)    
"""
from flask import Flask
from flask import render_template
from models import *
from models import storage


app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display HTML page: (inside the tag BODY)"""
    states = storage.all('State').values()
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)


@app.teardown_appcontext
def teardown_db(exception):
    """remove current sqlalchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
