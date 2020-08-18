# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
import DB_Config
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
mongo = DB_Config.mongo
APP_URL = "http://127.0.0.1:5000"


class Course(Resource):
    def get(self, Course_Id=None, Course_Name=None, Training_Id=None, Status=None,Created_At=None):
        data = []

        if Course_Id:
            Course_Id = mongo.course.find_one({"Course_Id": id}, {"_id": 0})
            if Course_Id:
                return jsonify({"status": "ok", "data": Course_Id})
            else:
                return {"response": "no course found for {}".format(Course_Id)}

        elif Training_Id:
            cursor = mongo.course.find({"Training_Id": Training_Id}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('course') + "/" + user.get('Training_Id')
                data.append(user)

            return jsonify({"Username": Training_Id, "response": data})

        elif Course_Name:
            cursor = mongo.course.find({"Course_Name": Course_Name}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('course') + "/" + user.get('Course_Name')
                data.append(user)

            return jsonify({"Course_Name": Course_Name, "response": data})

        elif Status:
            cursor = mongo.course.find({"Status": Status}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('course') + "/" + user.get('Status')
                data.append(user)

            return jsonify({"Status": Status, "response": data})

        elif Created_At:
            cursor = mongo.course.find({"Created_At": Status}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('course') + "/" + user.get('Created_At')
                data.append(user)

            return jsonify({"Status": Status, "response": data})

        else:
            cursor = mongo.course.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for user in cursor:
                user['url'] = APP_URL + url_for('course') + "/" + user.get('Course_Id')
                data.append(user)

            return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            Course_Id = data.get('Course_Id')

            if Course_Id != None:
                if mongo.course.find_one({"Course_Id": Course_Id}):
                    return {"response": "Course already exists."}
                else:
                    mongo.course.insert(data)
            else:
                return {"response": "id number missing"}

        return redirect(url_for("course"))

    def put(self, id):
        data = request.get_json()
        mongo.course.update({'id': id}, {'$set': data})
        return redirect(url_for("user"))

    def delete(self, id):
        mongo.course.remove({'id': id})
        return redirect(url_for("user"))


class Index(Resource):
    def get(self):
        return redirect(url_for("course"))


api = Api(app)
api.add_resource(Index, "/course/", endpoint="index")
api.add_resource(Course, "/api/course", endpoint="course")
api.add_resource(Course, "/api/course/<string:Course_Id>", endpoint="Course_Id")
api.add_resource(Course, "/api/course/Course_Name/<string:Course_Name>", endpoint="Course_Name")
api.add_resource(Course, "/api/Course/Training_Id/<string:Training_Id>", endpoint="Training_Id")



if __name__ == "__main__":
    app.run(debug=True)