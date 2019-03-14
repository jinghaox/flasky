from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    # here we use session['name'] to share variable between requests, it's global-like
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        # here is the redirect, after POST request(submission), redirect to index, so next time it will call GET if we
        # refresh the page, and it won't re-POST the data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))
