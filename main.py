from flask import Flask, render_template, request, redirect, url_for
import time
from datetime import datetime, timedelta
import random
from slugify import slugify

from google.appengine.ext import ndb

MAX_AGE = timedelta(minutes=10)

class Coin(ndb.Model):
	heads = ndb.BooleanProperty()
	date = ndb.DateTimeProperty(auto_now_add = True)
	
	@property
	def expiry(self):
		return self.date + MAX_AGE
	
	@property
	def expired(self):
		return datetime.utcnow() > self.expiry
 
app = Flask(__name__)

@app.route('/coin/<coin_id>')
def coin(coin_id):
	coin_slug = coin_id
	coin_slug = slugify(coin_id)
	if (coin_slug != coin_id):
		return redirect(url_for('coin', coin_id=coin_slug))
		
	key = ndb.Key(Coin, coin_slug)
	
	coin_obj = key.get()
	
	if coin_obj is not None and coin_obj.expired:
		coin_obj.key.delete()
		coin_obj = None
	
	if coin_obj is None:
		heads = random.choice([True, False])
		coin_obj = Coin(heads = heads, key = key)
		coin_obj.put()
		
	side_names = {True: "Heads", False: "Tails"}
	
	return render_template('coin.html', coin=coin_obj)
#	return "%s tossed at %s expires at %s" % (side_names[coin_obj.heads], coin_obj.date, coin_obj.date + max_age)		   

 
if __name__ == "__main__":
    app.run()