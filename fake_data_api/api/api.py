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
        parser.add_argument("date", type=str)  # better way to do that?
        date = parser.parse_args().get("date")
        return {
            "customers": db.get_customers(date),
            "transactions": db.get_transactions(date),
            "transaction_details": db.get_transaction_details(date),
        }


api.add_resource(FakerApi, "/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
