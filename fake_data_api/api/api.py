from flask import Flask
from flask_restful import Resource, Api, reqparse
from database.models.util import ApplicationDataBase


from faker import Faker

app = Flask(__name__)
api = Api(app)
fake = Faker()

db = ApplicationDataBase()


class FakerApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("date", type=str)
        parser.add_argument("table_name", type=str)
        table_name = parser.parse_args().get("table_name")
        date = parser.parse_args().get("date")
        return db.get_data(date, table_name)


api.add_resource(FakerApi, "/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
