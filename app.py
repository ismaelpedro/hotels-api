from flask import Flask
from flask_restful import Api
from resources.hotels import Hotel, Hotels, NewHotel
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
initialized = False

@app.before_request
def create_db():
    global initialized
    if not initialized:
        db.create_all()
        initialized = True

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<int:id>')
api.add_resource(NewHotel, '/hotels')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    CORS(app)
    app.run(debug=True)