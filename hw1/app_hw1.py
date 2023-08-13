from flask import Flask, render_template

app = Flask(__name__)


@app.route('/main/')
def main():
    context = {'title': 'Главная'}
    return render_template('main.html', **context)

@app.route('/Clother/')
def clother():
    context = {'title': 'Одежда'}
    return render_template('Clother.html', **context)

@app.route('/Shoes/')
def shoes():
    context = {'title': 'Обувь'}
    return render_template('Shoes.html', **context)

@app.route('/UpClother/')
def up_clother():
    context = {'title': 'Верхняя одежда'}
    return render_template('UpClother.html', **context)

if __name__ == '__main__':
    app.run()
