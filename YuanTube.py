import logging

from flask import Flask
from flask import render_template
from flask import request
from flask_script import Manager, Shell, Command
from flask import abort

app = Flask(__name__)

manager = Manager(app)

def make_shell_context():
    from models import db
    return dict(app=app, db=db)


# ----------------Error Handler----------------- #
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


# ----------------Error Handler----------------- #
@app.route('/error')
def error():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404


@app.route('/hello/<name>')
def hello_world(name=None):
    return render_template('hello_test.html', name=name)


# ----------------Config Options----------------- #
def configure_app():
    from config import key
    app.secret_key = key.secret_key
    from config.config import config_dict
    app.config.update(config_dict)
    register_routes(app)
    manager.add_command('shell', Shell(make_context=make_shell_context))
    # 设置 log, 否则输出会被 gunicorn 吃掉
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configured_app():
    configure_app()
    return app


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
    configure_app()
    manager.run()