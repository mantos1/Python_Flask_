from flask import Flask, render_template, request, redirect, url_for
import secrets
from flask_wtf.csrf import CSRFProtect
from models import db, User
from form import RegistrationForm
import hashlib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
app.secret_key = secrets.token_hex()
csrf = CSRFProtect(app)

@app.route('/')
def index():
    # return 'Hi!'
    return redirect(url_for('registration'))

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB created")

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    context = {
        'title': 'Форма регистрации'
    }
    form = RegistrationForm()
    if form.validate_on_submit():
        password = hashlib.sha256(form.password.data.encode(encoding='UTF-8')).hexdigest()
        user = User(lastname=form.lastname.data,
                    firstname=form.firstname.data,
                    email=form.email.data,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('registration'))
    return render_template('form.html', form=form, **context)

if __name__ == '__main__':
    db_folder = os.path.join(os.path.dirname(__file__), '.\\instance\\test.db')
    if not os.path.isfile(db_folder):
        with app.app_context():
            db.create_all()
    app.run()