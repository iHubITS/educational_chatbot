# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
import DB_Config
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
mongo = DB_Config.mongo
APP_URL = "http://127.0.0.1:5000"


class User(Resource):
    def get(self, id=None, Username=None, User_Email=None, User_Contact=None):
        data = []

        if id:
            user_info = mongo.user.find_one({"id": id}, {"_id": 0})
            if user_info:
                return jsonify({"status": "ok", "data": user_info})
            else:
                return {"response": "no user found for {}".format(id)}

        elif Username:
            cursor = mongo.user.find({"Username": Username}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('user') + "/" + user.get('id')
                data.append(user)

            return jsonify({"Username": Username, "response": data})

        elif User_Email:
            cursor = mongo.user.find({"User_Email": User_Email}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('user') + "/" + user.get('id')
                data.append(user)

            return jsonify({"User_Email": User_Email, "response": data})

        elif User_Contact:
            cursor = mongo.user.find({"User_Contact": User_Contact}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('user') + "/" + user.get('id')
                data.append(user)

            return jsonify({"User_Contact": User_Contact, "response": data})

        else:
            cursor = mongo.user.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for user in cursor:
                user['url'] = APP_URL + url_for('user') + "/" + user.get('id')
                data.append(user)

            return jsonify({"response": data})

    def post(self):

        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            id = data.get('id')

            if id != None:
                if mongo.user.find_one({"id": id}):
                    return {"response": "user already exists."}
                else:
                    mongo.user.insert(data)
            else:
                return {"response": "id number missing"}

        return redirect(url_for("user"))

    def put(self, id):
        data = request.get_json()
        mongo.user.update({'id': id}, {'$set': data})
        return redirect(url_for("user"))

    def delete(self, id):
        mongo.user.remove({'id': id})
        return redirect(url_for("user"))


class Index(Resource):
    def get(self):
        return redirect(url_for("user"))

class Index1(Resource):
    def get(self):
        return redirect(url_for("Training_details"))


api = Api(app)
api.add_resource(Index, "/user/", endpoint="index")
api.add_resource(User, "/api/user/", endpoint="user")
api.add_resource(User, "/api/user/<string:id>", endpoint="id")
api.add_resource(User, "/api/user/Username/<string:Username>", endpoint="Username")
api.add_resource(User, "/api/user/User_Email/<string:User_Email>", endpoint="User_Email")
api.add_resource(User, "/api/user/User_Contact/<string:User_Contact>", endpoint="User_Contact")


if __name__ == "__main__":
    app.run(debug=True)