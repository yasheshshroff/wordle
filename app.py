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
    # Sanitie the input into lower case & remove all non-ascii characters
    use = request.form['use'].lower()
    use = set(re.sub(r'[^a-z]', '', use))

    avoid = request.form['avoid'].lower()
    avoid = set(re.sub(r'[^a-z]', '', avoid))
    p = [None] * 5
    pattern = ""
    for index in range(5):
        place = 'place' + index + 1
        p[index] = request.form[place].lower()
        p[index] = re.sub(r'[^a-z]', '', p[index])
        if len(p[index]) > 1):
            p[index] = p[index][0]
        if p[index]:
            pattern = pattern + p[index]
        else:
            pattern = pattern + "."
    # Exit if input is contradictory or too long
    common_letters = list(set(avoid) & set(use))
    no_error = True
    messages = []
    if (len(common_letters) > 0 ):
        messages.append(f"You are asking me to find words with letters to be used AND avoided: {', '.join(common_letters)}. Retry")
        no_error = False 
    if (len(use) > 5):
        messages.append(f"The number of letters that must be used cannot be greater than 5. Retry")
        no_error = False
    if (not no_error):
        return render_template('index.html', headers=messages, results="લાલ્લૂ માસ્ટર")

    # Find all words in list p that include all the letters in pattern in any order
    results = p.copy()
    messages.append(f"Started with {len(results)} words")

    # Work on the known pattern
    results = [x for x in results if re.search(pattern, x)]
    messages.append(f"Filtered to {len(results)} words with pattern {pattern}")

    for c in set(use):
        results = [x for x in results if re.search("(?=.*" + c + ").*", x)]
        messages.append(f"Filtered to {len(results)} words with {c}")
    for c in set(avoid):
        results = [x for x in results if not re.search("(?=.*" + c + ").*", x)]
        messages.append(f"Filtered to {len(results)} words without {c}")

    return render_template('index.html',
        headers=messages,
        results=", ".join(results))

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
