from flask import Flask

app = Flask(__name__)


@app.route('/hello/<int:user_id>')
def hello_world(user_id):
    return 'User ID: %d' % user_id


if __name__ == '__main__':
    app.run()