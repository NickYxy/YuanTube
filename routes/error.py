__author__ = 'nickyuan'
from . import *
from flask import current_app as app
from flask import abort
from flask import Flask
from flask import render_template


# ----------------Error Handler----------------- #
@app.route('/error')
def error():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'),404
