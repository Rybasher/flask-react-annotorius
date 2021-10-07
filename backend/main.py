from flask import Blueprint
from . import db
from . import create_app


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return 'Index'

@main.route('/profile')
def profile():
    return 'Profile'


if __name__ == "__main__":
    create_app().run()
