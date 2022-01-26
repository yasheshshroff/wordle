"""
A Flask application that routes user input to the appropriate function.
"""
import os

from flask import Flask, render_template, request

from english_words import english_words_lower_alpha_set

import re
p = [word for word in english_words_lower_alpha_set if len(word)==5]

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "Let's wordle!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

# Write a method to handle flask post request taking user input "word" from a form    
@app.route('/wordle', methods=['POST'])
def wordle():
    """
    Return render_template that takes user input "pattern" from a form and regex matches all words in p that include all letters in "pattern" in any order. 
    For instance, if pattern = "ab", then the regex should match "ab", "ba", "abc", "bac", "cab", "cba", etc.
    """
    use = request.form['use']
    avoid = request.form['avoid']
    # Find all words in list p that include all the letters in pattern in any order
    results = p.copy()
    messages = []
    messages.append(f"Starting with {len(results)} words")
    for c in use:
        results = [x for x in results if re.search("(?=.*" + c + ").*", x)]
        messages.append(f"Filtered to {len(results)} words with {c}")
    for c in avoid:
        results = [x for x in results if not re.search("(?=.*" + c + ").*", x)]
        messages.append(f"Filtered to {len(results)} words with {c}")
    # Return render_template that takes user input "pattern" from a form and regex matches all words in p that include all letters in "pattern" in any order. 
    return render_template('index.html',
        header=messages,
        results=results)


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
    
    p = ["abc", "bcd", "cab", "def", "fga", "asa"]
    pattern = "ab"
    # Write a forward looking regular expression (?=) to find a sublist of all words in p that include all letters in pattern in any order. 
    # For instance, if pattern = "ab", then the regex should match "ab", "ba", "abc", "bac", "cab", "cba", etc.






