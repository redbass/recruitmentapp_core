from flask import Flask

from api.route import add_routes

app = Flask(__name__)
add_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
