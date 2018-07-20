from . import *
from models.movie import Movies, MovieCategory

main = Blueprint('movie', __name__)


# ------------------------- 电影分类管理 --------------------------

@main.route('/course/category/new', methods=['POST'])
@admin_required
def category_new():
    form = request.form
    status, msgs = MovieCategory.valid(form)
    if status is True:
        MovieCategory.new(form)
        return redirect(url_for('movie.category'))
    else:
        flash('该分类已存在！', 'warning')
        return redirect(url_for('movie.category'))


@main.route('/course/category')
@admin_required
def category():
    u = current_user()
    c = MovieCategory.all()
    return render_template('admin/movie_category.html', c=c, u=u)


@main.route('/category/del/<uuid>')
@admin_required
def category_del(uuid):
    m = MovieCategory.get_uuid(uuid)
    m.delete()
    return redirect(url_for('movie.category'))


# todo 查看分类下的课程？
@main.route('/category/<uuid>', methods=['POST'])
@admin_required
def category_update(uuid):
    p = MovieCategory.find_one(uuid=uuid)
    l = []
    ms = Movies.all()
    for m in ms:
        if m.category_uuid == p.category_uuid:
            l.append(m)
    return redirect(url_for('movie.movies', uuid=p.uuid))


# ------------------------- 电影管理 --------------------------

@main.route('/movies')
@admin_required
def movies():
    u = current_user()
    m = Movies.all()
    return render_template('admin/movie_list.html', m=m, u=u)


@main.route('movie/add', methods=['POST'])
@admin_required
def movie_add():
    pass
