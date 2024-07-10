#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from views.index import *
from views.states import *
