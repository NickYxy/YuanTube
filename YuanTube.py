from flask import Flask
from flask import render_template
from flask import request
from flask_script

app = Flask(__name__)

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