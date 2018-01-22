from flask import Flask, render_template, request, redirect, url_for, make_response
import time
from datetime import datetime, timedelta
from flask.views import MethodView
import random
from .raffle import Raffle, RaffleAlreadyExists, MAX_AGE
from collections import OrderedDict

app = Flask(__name__)

@app.route('/raffle/<raffle_id>', methods=('GET',))
def raffle_detail_view(raffle_id):
    raffle = Raffle.retrieve(raffle_id)

    if raffle is None:
        return index_view(error="Raffle not found"), 404
    return render_template('raffle.html', raffle=raffle)

@app.route('/raffle/', methods=('POST','GET'))
def raffle_creation_view():
    if request.method == "GET":
        return redirect(url_for('index_view'))
    else: 
        form = request.form
        try:
            raffle_id = form['raffle_id']
            max_age = int(form['max_age'])
            deduplicate = form.get('deduplicate', None) is not None
            choices = form['choices']
        except KeyError, ValueError:
            return index_view(error="Form invalid."), 400
        if len(raffle_id) == 0:
            return index_view(error="A Raffle ID is required"), 400
        if max_age < 0 or max_age > MAX_AGE:
            return index_view(error="The expiry length is invalid"), 400
        choices = choices.split('\n')
        choices = [choice.strip() for choice in choices if len(choice.strip()) > 0]
        if deduplicate:
            choices = OrderedDict([(choice,None) for choice in choices]).keys()
        if len(choices) < 2:
            return index_view(error="Two or more choices required."), 400
        try:
            raffle = Raffle.create(raffle_id, choices, max_age)
        except RaffleAlreadyExists:
            return index_view(error="Raffle with ID already exists"), 409

        return redirect(url_for('raffle_detail_view', raffle_id = raffle.raffle_id), code=303)

@app.route('/')
def index_view(error=None):
    return render_template('index.html', error=error)