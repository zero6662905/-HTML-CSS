from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    return "<h1>Hello, world!</h1>"

@app.route("/about/")
def about():
    return "<h1>Про нас</h1>"

@app.route("/services/")
def services():
    return "<h1>опис послуг</h1>"

@app.route("/contact/")
def contact():
    return "<h1>Контактна сторінка з інформацією про зв'язок</h1>"

if __name__ == '__main__':
    app.run(debug=True)