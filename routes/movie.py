from . import *
from models.movie import Movie

main = Blueprint('movie', __name__)


@main.route('/detail/<uuid>')
@login_required
def detail(uuid):
    u = current_user()
    p = Movie.find_one(uuid=uuid)

    return render_template('video/movies.html', p=p, u=u, cats=get_cats())


@main.route('/category/<category>')
@login_required
def products(category):
    u = current_user()
    ps = Movie.find(category=category)
    return render_template('video/movies.html', ps=ps, u=u, category=category, cats=get_cats())
