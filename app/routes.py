from flask import render_template

from app import app


@app.route('/')
@app.route('/index')
def index():

    context = {
        'title': 'Home',
    }

    return render_template('index.html', **context)