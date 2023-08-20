from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = b'66c2c3078ce4d1dc840f1c944519146f657580d3edcce2acb0810c1e10bb9add'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.app_context().push()
db.create_all()


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        save_info(name, last_name, email, password)
    return render_template('register.html', form=form)


def save_info(name, last_name, email, password):
    user = User(name=name, last_name=last_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
