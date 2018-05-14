import logging

from flask import Flask
from flask import render_template
from flask import request
from flask_script import Manager, Shell, Command
from flask import abort

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


#----------------Error Handler-----------------#
@app.route('/error')
def error():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404


@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello_test.html', name=name)

@manager.command
def server():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=8001,
    )
    app.run(**config)

if __name__ == '__main__':
    manager.run()