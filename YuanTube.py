import logging

from flask import Flask
from flask import render_template
from flask import request
from flask_script import Manager, Shell, Command

app = Flask(__name__)

manager = Manager(app)


def make_shell_context():
    from models import db
    return dict(app=app, db=db)


# ----------------BluePrints Register----------------- #
def register_routes(app):
    from routes.index import main as routes_index
    from routes.user import main as routes_user
    from routes.movie import main as routes_movie
    from routes.admin import main as routes_admin
    from routes.img import main as routes_img

    app.register_blueprint(routes_user, url_prefix='/user')
    app.register_blueprint(routes_index, url_prefix='/')
    app.register_blueprint(routes_movie, url_prefix='/movie')
    app.register_blueprint(routes_admin, url_prefix='/admin')
    app.register_blueprint(routes_img, url_prefix='/img')


def register_filters(app):
    from user_util.filters import filters
    app.jinja_env.filters.update(filters)


# ----------------Config Options----------------- #
def configure_app():
    from config import key
    app.secret_key = key.secret_key
    from config.config import config_dict
    app.config.update(config_dict)
    register_routes(app)
    register_filters(app)
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
    # 当 static 文件夹中的文件修改时，响应 200，避免浏览器的主动缓存策略
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.jinja_env.auto_reload = True
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=8003,
    )
    app.run(**config)


if __name__ == '__main__':
    configure_app()
    manager.run()
