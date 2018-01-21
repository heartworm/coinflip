from flask import Flask, render_template, request, redirect, url_for
import time
from datetime import datetime, timedelta
from flask.views import MethodView
import random
from .raffle import Raffle

app = Flask(__name__)

@app.route('/raffle/<raffle_id>', methods=('GET',))
def raffle_detail_view(raffle_id):
    pass

@app.route('/raffle/', methods=('POST',))
def raffle_creation_view():
    pass

@app.route('/')
def index():
    return render_template('index.html')