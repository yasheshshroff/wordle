from flask import Flask, render_template, request
from english_words import english_words_lower_alpha_set
import re

app = Flask(__name__)

p = [word for word in english_words_lower_alpha_set if len(word)==5]
messages = [{'title': '^',
             'content': 'Beginning of the pattern'},
             {'title': '[a-z]',
                 'content': 'letters to include, can be a range'},
             {'title': '[^a-z]',
                 'content': 'letters to NOT include, can be a range'},
             {'title': '.',
                 'content': 'a single dot (.) represents a single letter'},
             ]

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    regex = request.form['pattern']
    #regex = "^ro[t^us]?[t^us]?[t^us]?"
    r = re.compile(regex)
    results = list(filter(r.match, p))
    return render_template('index.html', results=results)
