import logging

from flask import Flask
from flask import render_template
from flask import request
from flask_script import Manager, Shell, Command


app = Flask(__name__)

manager = Manager(app)

#import blueprints

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return 'This is a post request'
    else:
        return 'This is a get request'

@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello_test.html', name=name)


if __name__ == '__main__':
    app.run()