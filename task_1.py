from flask import Flask


app = Flask(__name__)

@app.route("/")
def main():
    return "Hello, world!"

@app.route("/about/")
def about():
    return "we teach programming"

@app.route("/services/")
def services():
    return "we teaching programming on python,javascript,c++,c#"

@app.route("/contact/")
def contact():
    return "example_email@gmail.com"


if __name__ == "__main__":
    app.run(debug=True)

