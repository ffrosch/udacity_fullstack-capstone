from flask import Blueprint
from flask import current_app as app

view = Blueprint('view', __name__)


@view.route('/')
def hello_world():
    return 'Hello, World!'
