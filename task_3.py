from flask import Flask, request, jsonify
import unittest

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get("username") == "admin" and data.get("password") == "secret":
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_successful_login(self):
        # Test with correct credentials
        response = self.client.post('/login', json={"username": "admin", "password": "secret"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Login successful"})

if __name__ == '__main__':
    unittest.main()