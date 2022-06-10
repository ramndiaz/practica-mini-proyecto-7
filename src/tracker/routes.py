from flask import Flask, jsonify, request, Response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_cors import CORS, cross_origin
from datetime import datetime
from bson import json_util
from __main__ import app
from app import mongo
import uuid

@cross_origin
@app.route('/createpomodoro', methods=['POST'])
@jwt_required(optional=False)
def create_pomodoro():
    user_id = request.json['user_id']
    if mongo.db.users.find_one({ "id": user_id }):
        task_id = uuid.uuid4().hex
        date_time = datetime.now()
        title = request.json['title']
        description = request.json['description']
        total_pomo = request.json['total_pomo']
        type_pomo = request.json['type_pomo']
    else:
        response = jsonify({ "error":"the provided user does not exist" })
        return response

    if task_id and user_id  and date_time and title and description and total_pomo and type_pomo:

        if int(total_pomo)> 0:
            mongo.db.pomodoro.insert_one({
                'task_id': task_id,
                'user_id': user_id,
                'date_time' : date_time,
                'title' : title,
                'description' : description,
                'type_pomo': type_pomo,
                'total_pomo' : total_pomo
                })
            response = jsonify({"msg": "pomodoro created successfully"})
            return response
        else:
            response = jsonify({ "error":"must save at least 1 full pomodoro." })
            return response
    else:
        response = jsonify({"error": "data could not be captured"})
        return response

@cross_origin
@app.route('/getpomodoros', methods=['GET'])
@jwt_required(optional=False)
def get_pomodoros():
    pomodoro = mongo.db.pomodoro.find()
    response = json_util.dumps(pomodoro)
    return Response(response, mimetype='application/json')

@cross_origin
@app.route('/gettracker', methods=['GET'])
@jwt_required(optional=False)
def get_tracker():
    tracker =  mongo.db.pomodoro.aggregate( [
   {
     "$lookup":
       {
         "from": "users",
         "localField": "user_id",
         "foreignField": "id",
         "as": "users and pomodoros"
       }
  }
] )
    response = json_util.dumps(tracker)
    return Response(response, mimetype='application/json')

@cross_origin
@app.route('/getpomodoro/<id>', methods=['GET'])
@jwt_required(optional=False)
def get_pomodoro(id):
    pomo = mongo.db.pomodoro.find({'user_id': id})
    response = json_util.dumps(pomo)
    return Response(response, mimetype='application/json')