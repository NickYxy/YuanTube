from . import *
from models.movie import Movies

main = Blueprint('movie', __name__)


@main.route('/movies')
@admin_required
def movies():
    u = current_user()
    m = Movies.all()
    return render_template('admin/movie_list.html', m=m, u=u)


@main.route('movie/add', method=['POST'])
@admin_required
def movie_add():
    pass
