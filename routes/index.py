__author__ = 'nickyuan'
from . import *

main = Blueprint('index', __name__)


@main.route('index')
@login_required
def index():
    u = current_user()
    return render_template('index.html', u=u)