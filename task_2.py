from flask import Flask, render_template, url_for, abort, redirect
import random
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return "Такої сторінки не існує!", 404

@app.route('/')
def home():
    return render_template("index2.html")

@app.route('/films/<id>/')
def film_profile(id):
    return render_template(f"film_{format(id)}.html")

@app.route('/random')
def random_film():
    ran = random.randint(0, 4)
    return redirect(url_for('film_profile', id=ran))

if __name__ == '__main__':
    app.run(debug=True)