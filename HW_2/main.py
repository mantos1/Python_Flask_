from flask import Flask, render_template, request, redirect, url_for, session, make_response
import secrets

app = Flask(__name__)
# secret_key = secrets.token_hex()
app.secret_key = secrets.token_hex()

@app.route('/')
def hello():
    if 'username' in session:
        context = {
            'username': session['username'],
            'email': session['email'],
            'title': 'Вы авторизованы!'
        }
        response = make_response(render_template('result.html', **context))
        response.set_cookie('username', context['username'])
        response.set_cookie('email', context['email'])
        return response

    return redirect(url_for('submit_form'))

@app.route('/submit_form/', methods = ['GET', 'POST'])
def submit_form():
    context = {
        'username': '',
        'email': '',
        'title': 'Форма авторизации'
    }
    if 'username' in session:
        return redirect(url_for('logout'))
    if request.method == 'POST':
        session['username'] = request.form.get('username') or 'NoName'
        session['email'] = request.form.get('email') or 'NoEmail'
        return redirect(url_for('hello'))

    response = make_response(render_template('form.html', **context))
    response.set_cookie('username', context['username'])
    response.set_cookie('email', context['email'])
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('hello'))

if __name__ == '__main__':
    app.run(debug=True)
