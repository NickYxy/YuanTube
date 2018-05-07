from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return 'This is a post request'
    else:
        return 'This is a get request'

@app.route('/hello/<int:user_id>')
def hello_world(user_id):
    return 'User ID: %d' % user_id


if __name__ == '__main__':
    app.run()