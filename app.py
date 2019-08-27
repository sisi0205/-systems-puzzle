import datetime
import os

from flask import Flask, render_template, redirect, url_for, request
from forms import ItemForm
from models import Items
from database import db_session


app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        # url=my_url_for('success',_external=True)
        # return url
        return redirect(my_url_for('success', _external=True))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    
    results = []
    qry = db_session.query(Items)
    # results = qry.all()
    for item in qry.all():
        results.append([item.name, item.quantity, item.description, item.date_added])
    return str(results)

def my_url_for(*args, **kwargs):
    with app.test_request_context():
        # With the test request context of the app
        kwargs['_external'] = True   
        url = url_for(*args, **kwargs)    # Get the URL
        ###correct the address
        url = url.replace('://localhost/', '://localhost:%d/' % (8080))   
        return url
  

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)
