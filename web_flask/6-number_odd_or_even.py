#!/usr/bin/python3
"""Script that starts a Flask web application:
    - web application must be listening on 0.0.0.0, port 5000
    - Routes:
        - /: display "Hello HBNB!"
        - /hbnb: display "HBNB"
        - /c/<text>: display "C" followed by the value of the text variable
        - /python/(<text>): display "Python", followed by the value of the
            text variable
            - The default value of text is "is cool"
        - /number/<n>: display "n is a number" only if n is an integer
        - /number_template/<n>: display a HTML page only if n is an integer
            - H1 tag: "Number: n" inside the tag BODY
        - /number_odd_or_even/<n>: display a HTML page only if n is an integer
            - H1 tag: "Number: n is even|odd" inside the tag BODY
"""
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """display "Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """display "HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """display C followed by value of the <text> variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is cool'):
    """display python followed by value of the <text> variable"""
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """display n is a number only if n is an integer"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """display HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """display HTML page only if n is an integer"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
