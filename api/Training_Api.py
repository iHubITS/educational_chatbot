from flask import Flask, jsonify, url_for, redirect, request
import DB_Config
from flask_restful import Api, Resource

app = Flask(__name__)
mongo = DB_Config.mongo
APP_URL = "http://127.0.0.1:5000/Training_Api"


class Training_details(Resource):
    def get(self, Training_Details_Id=None, User_Id=None, Course_Id=None, Training_Status=None,Quiz_Marks=None,Created_At=None):
        data = []
        combine_data = []
        if Training_Details_Id:
            Training_Details_data = mongo.Training_details.find_one({"Training_Details_Id": Training_Details_Id}, {"_id": 0})
            if Training_Details_data:
                User_data = mongo.user.find_one({"id": str(Training_Details_data["User_Id"])},{"_id": 0})
                Course_data = mongo.course.find_one({"Course_Id": Training_Details_data["Course_Id"]}, {"_id": 0})

                combine_data = dict(
                    Training_Details_Id=Training_Details_data["Training_Details_Id"],
                    User_Id=Training_Details_data["User_Id"],
                    Course_Id=Training_Details_data["Course_Id"],
                    Training_Status=Training_Details_data["Training_Status"],
                    Course_Name=Course_data["Course_Name"],
                    Training_Id=Course_data["Training_Id"],
                    Username =User_data["Username"],
                    User_Email=User_data["User_Email"],
                    )
                return jsonify({"status": "ok", "data": combine_data})
            else:
                return {"response": "no training details found for {}".format(Training_Details_Id)}

        elif User_Id:
            cursor = mongo.Training_details.find({"User_Id": User_Id}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('Training_Details') + "/" + Training_details.get('User_Id')
                data.append(user)

            return jsonify({"Username": User_Id, "response": data})

        elif Course_Id:
            cursor = mongo.Training_details.find({"Course_Id": Course_Id}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('Training_details') + "/" + Training_details.get('Course_Id')
                data.append(user)

            return jsonify({"Course_Id": Course_Id, "response": data})

        elif Training_Status:
            cursor = mongo.course.find({"Status": Training_Status}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('Training_details') + "/" + Training_details.get('Training_Status')
                data.append(user)

            return jsonify({"Status": Training_Status, "response": data})

        elif Quiz_Marks:
            cursor = mongo.course.find({"Quiz_Marks": Quiz_Marks}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('Training_details') + "/" + Training_details.get('Quiz_Marks')
                data.append(user)

            return jsonify({"Status": Quiz_Marks, "response": data})

        elif Created_At:
            cursor = mongo.Training_details.find({"Created_At": Created_At}, {"_id": 0}).limit(10)
            for user in cursor:
                user['url'] = APP_URL + url_for('Training_details') + "/" + Training_details.get('Created_At')
                data.append(user)

            return jsonify({"Status": Created_At, "response": data})

        else:
            cursor = mongo.Training_details.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for user in cursor:
                user['url'] = APP_URL + url_for('Training_details') + "/" + Training_details.get('_id')
                data.append(user)

            return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            Training_Details_Id = data.get('Training_Details_Id')

            if Training_Details_Id != None:
                if mongo.db.Training_details.find_one({"Training_Details_Id": Training_Details_Id}):
                    return {"response": "Training_details already exists."}
                else:
                    mongo.Training_details.insert(data)
            else:
                return {"response": "id number missing"}

        return redirect(url_for("Training_details"))

    def put(self, Training_Details_Id):
        data = request.get_json()
        mongo.Training_details.update({'Training_Details_Id': Training_Details_Id}, {'$set': data})
        return redirect(url_for("Training_details"))

    def delete(self, Training_Details_Id):
        mongo.Training_details.remove({'Training_Details_Id': Training_Details_Id})
        return redirect(url_for("Training_details"))


class Index(Resource):
    def get(self):
        return redirect(url_for("Training_details"))


api = Api(app)
api.add_resource(Index, "/Training_Api/", endpoint="index")
api.add_resource(Training_details, "/api/Training_Api/", endpoint="Training_details")
api.add_resource(Training_details, "/api/Training_Api/<string:Training_Details_Id>", endpoint="Training_Details_Id")




if __name__ == "__main__":
    app.run(debug=True)