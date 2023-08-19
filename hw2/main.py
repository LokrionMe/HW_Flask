from flask import Flask, redirect, request, render_template, make_response

app = Flask(__name__)


@app.get('/login/')
def submit_get():
    return render_template('login.html')


@app.post('/login/')
def submit_post():
    name = None
    post = None
    name = request.form.get('name')
    post = request.form.get('post')
    if name == None or post == None:
        return redirect('/login/')
    else:
        res = make_response(redirect('/main/'))
        res.set_cookie('user', name)
        res.set_cookie('email', post)
        return res


@app.route('/del_login/')
def pop_cookies():
    response = make_response(redirect('/login/'))
    response.delete_cookie('user')
    response.delete_cookie('email')
    return response


@app.route('/main/')
def main_page():
    if request.cookies.get('user') and request.cookies.get('email'):
        name = request.cookies.get('user')
        post = request.cookies.get('email')
        return render_template('main.html', name=name, post=post)
    else:
        return redirect('/login/')


app.run()
