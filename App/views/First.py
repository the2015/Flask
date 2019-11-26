from flask import Blueprint, render_template, request, session
from App.models import db, User

blue = Blueprint('blue', __name__)


# #
# @blue.route('/')
# def index():
#     return render_template('2.html')


@blue.route('/db')
def createDb():
    db.create_all()
    return 'success'


@blue.route('/test/<username>')
def addUser(username):
    # user = User()
    # user.username = username
    # user.password = '12456'
    # user.save()
    return username


@blue.route('/test/<string:username>/')
def test(username):
    # user = User()
    # user.username = username
    # user.password = '12456'
    # user.save()
    return username


@blue.route('/Test/')
def get_request():
    print(request.host)
    print(request.cookies)
    print(session)
    return 'request'


@blue.route('/user/')
def get_user():
    # user = User.query.get_or_404(4)
    # return user.username
    # user = User.query.get(2)
    # return user.username
    user = User.query.all()
    # for u in user:
    #     print(u.username)
    return render_template("2.html", User=user)


@blue.route('/del/')
def del_user():
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "ok"


@blue.route('/up/')
def up_user():
    user = User.query.get(2)
    user.username = "yyf"
    db.session.add(user)
    db.session.commit()
    return "ok"
