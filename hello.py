from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from markupsafe import Markup
import socket
import os
from werkzeug.user_agent import UserAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your first name?', validators=[DataRequired()])
    sobrenome = StringField('What is your last name?', validators=[DataRequired()])
    prontuario = StringField('What is your student ID?', validators=[DataRequired()])
    instituicao = StringField('What is your institution?', validators=[DataRequired()])
    discipline = StringField('What is your discipline name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['sobrenome'] = form.sobrenome.data
        session['prontuario'] = form.prontuario.data
        session['instituicao'] = form.instituicao.data
        session['discipline'] = form.discipline.data
        return redirect(url_for('index'))
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    user_agent = UserAgent(request.headers.get('User-Agent'))
    return render_template('index.html', form=form, name=session.get('name'), sobrenome=session.get('sobrenome'), prontuario=session.get('prontuario'), instituicao=session.get('instituicao'), discipline=session.get('discipline'), ip=ip, user_agent=user_agent)
