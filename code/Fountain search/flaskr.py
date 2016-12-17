import os
from elasticsearch import Elasticsearch
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create our little application :)
app = Flask(__name__)
query = None

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=Elasticsearch(),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    """Connects to the specific database."""
    rv = app.config['DATABASE']
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'elastic'):
        g.elastic = connect_db()
    return g.elastic

def init_db():
    db = get_db()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print ('Initialized the database.')


@app.route('/', defaults={'query':None})
@app.route('/<query>')
def show_entries(query):
    db = get_db()
    if query:
        cur = db.search(index='index', doc_type='news', q=query)
        entries = [{'title' : hit['_source']['title'], 'text' : hit['_source']['content']} for hit in cur['hits']['hits']]
    else:
        entries = []
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    txt = request.form['text']
    query = txt
    return redirect(url_for('show_entries', query=query))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
