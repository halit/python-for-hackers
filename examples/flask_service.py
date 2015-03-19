from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', 'null')
        password = request.form.get('password', 'null')
        if username == 'root' and password == 'toor':
            return jsonify({'msg': 'Welcome to secret panel'})
        else:
            return jsonify({'msg': 'Access denied'})
    else:
        return jsonify({'msg': 'Please login.'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)