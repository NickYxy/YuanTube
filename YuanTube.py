import logging

from flask import Flask
from flask import render_template
from flask import request
from flask_script import Manager, Shell, Command


app = Flask(__name__)

manager = Manager(app)

#import blueprints
def register_routes(app):
    from routes.user import main as routes_user
    from routes.movie import main as routes_movie
    from routes.admin import main as routes_admin


    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_movie, url_prefix='/movie')
    app.register_blueprint(routes_admin, url_prefix='/admin')



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