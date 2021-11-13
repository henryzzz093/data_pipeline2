import numpy as np
from flask import Flask
from flask_restful import Resource, Api

from faker import Faker

app = Flask(__name__)
api = Api(app)
fake = Faker()


class FakerApi(Resource):
    def get(self):
        return self.get_customer()

    def get_email(self, name):
        first_name = name.split()[0]
        last_name = name.split()[-1]

        index = np.random.randint(0, 3)
        domains = ["gmail", "yahoo", "outlook"]
        email = f"{first_name}.{last_name}@{domains[index]}.com"
        return email.lower()

    def get_customer(self):
        name = fake.name()
        address = fake.address()
        phone = fake.phone_number().split("x")[0]
        email = self.get_email(name)
        return {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
        }


api.add_resource(FakerApi, "/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
