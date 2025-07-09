from flask import Flask, jsonify

app = Flask(__name__)
app.logger.setLevel("INFO")


@app.route('/error', methods=['GET'])
def error():
    app.logger.error("Error route triggered!")
    return jsonify({"error": "Something went wrong"}), 500

if __name__ == '__main__':
    app.run(debug=True)