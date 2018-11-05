from flask import Flask
from flask_restful import Resource, Api
import csv

app = Flask(__name__)
api = Api(app)


class Cats(Resource):
    def __init__(self):
        self.existing_cats = []
        self.cat_dict = self.read_csv()

    def read_csv(self):
        cat_dict = {}
        with open('cat_list.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.existing_cats = [(x[0], x[1]) for x in csv_reader if x != []]
        for cat in self.existing_cats:
            cat_dict[cat[0]] = cat[1]
        return cat_dict

    def get(self):
        return self.cat_dict


api.add_resource(Cats, '/')

if __name__ == "__main__":
    app.run(debug=True)