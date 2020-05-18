"""Flask site for Balloonicorn's Party."""

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from partyutil import is_mel, most_and_least_common_type

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

# One day I'll move this to a database --Balloonicorn
TREATS = [{'type': 'dessert',
           'description': 'Chocolate mousse',
           'who': 'Andrew'},
          {'type': 'dessert',
           'description': 'Cardamom-Pear pie',
           'who': 'Kat'},
          {'type': 'appetizer',
           'description': 'Humboldt Fog cheese',
           'who': 'Meggie'},
          {'type': 'dessert',
           'description': 'Lemon bars',
           'who': 'Marisa'},
          {'type': 'appetizer',
           'description': 'Mini-enchiladas',
           'who': 'Rome'},
          {'type': 'drink',
           'description': 'Sangria',
           'who': 'Anges'},
          {'type': 'dessert',
           'description': 'Chocolate-raisin cookies',
           'who': 'Hayley'},
          {'type': 'dessert',
           'description': 'Brownies',
           'who': 'Ashley'}]


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/treats')
def show_treats():
    """Show treats people are bringing."""

    most, least = most_and_least_common_type(TREATS)

    return render_template('treats.html',
                           treats=TREATS,
                           most=most,
                           least=least)


@app.route('/rsvp', methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get('name')
    email = request.form.get('email')

    if not is_mel(name, email):
        session['rsvp'] = True
        flash('Yay!')
        return redirect('/')

    else:
        flash('Sorry, Mel. This is kind of awkward.')
        return redirect('/')


if __name__ == '__main__':
    app.debug = True
    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')
