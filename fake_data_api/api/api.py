import numpy as np
from flask import Flask
from flask_restful import Resource, Api

from faker import Faker

app = Flask(__name__)
api = Api(app)
fake = Faker()


class FakerApi(Resource):
    def get(self):
        data = []
        num_customers = np.random.randint(0, 10)
        for i in range(num_customers):
            data.append(self.get_customer())
        return data

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

    def get_num_products(self):
        data = []
        num_products = np.random.randint(0, 10)
        for i in range(num_products):
            data.append(self.num_products())
        return data

    def get_num_stores(self):
        data = []
        num_stores = np.random.randint(0, 10)
        for i in range(num_stores):
            data.append(self.num_stores())
        return data

    def get_stores(self):
        store_address = fake.address()

        return {
            "store_address": store_address,
        }

    def get_transactions(self):
        pass


api.add_resource(FakerApi, "/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
