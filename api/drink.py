import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.drinks import Drink

drink_api = Blueprint('drink_api', __name__,
                   url_prefix='/api/drinks')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(drink_api)

class DrinkyAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        @token_required
        def post(self, current_user): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate drinkName
            drinkName = body.get('drinkName')
            if drinkName is None or len(drinkName) < 2:
                return {'message': f'drinkName is missing, or is less than 2 characters'}, 400
            # validate uid
            calories = body.get('calories')
            if calories is None or calories < 0 :
                return {'message': f'calories has to be positive number'}, 400

            ''' #1: Key code block, setup USER OBJECT '''
            newDrink = Drink(drinkName=drinkName, 
                      calories=calories)
            
            ''' #2: Key Code block to add user to database '''
            # create drink in database
            just_added_drink = newDrink.create()
            # success returns json of user
            if just_added_drink:
                return jsonify(just_added_drink.read())
            # failure returns error
            return {'message': f'Processed {drinkName}, either a format error or it is duplicate'}, 400

        def get(self, current_user, lname=None):  # Updated method with lname parameter
            if lname:
                drinkName = Drink.query.filter_by(lname=lname).first()  # Adjust this based on your model attributes
                if drinkName:
                    return jsonify(drinkName.read())  # Assuming you have a read() method in your DrinkyApi model
                else:
                    return jsonify({"message": "Drink not found"}), 404
            else:
                drinks = Drink.query.all()    # read/extract all users from the database
                json_ready = [drink.read() for drink in drinks]  # prepare output in json
                return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

   
    # class _Security(Resource):
    #     def post(self):
    #         try:
    #             body = request.get_json()
    #             if not body:
    #                 return {
    #                     "message": "Please provide user details",
    #                     "data": None,
    #                     "error": "Bad request"
    #                 }, 400
    #             ''' Get Data '''
    #             uid = body.get('uid')
    #             if uid is None:
    #                 return {'message': f'User ID is missing'}, 400
    #             password = body.get('password')
                
    #             ''' Find user '''
    #             user = User.query.filter_by(_uid=uid).first()
    #             if user is None or not user.is_password(password):
    #                 return {'message': f"Invalid user id or password"}, 400
    #             if user:
    #                 try:
    #                     token = jwt.encode(
    #                         {"_uid": user._uid},
    #                         current_app.config["SECRET_KEY"],
    #                         algorithm="HS256"
    #                     )
    #                     resp = Response("Authentication for %s successful" % (user._uid))
    #                     resp.set_cookie("jwt", token,
    #                             max_age=3600,
    #                             secure=True,
    #                             httponly=True,
    #                             path='/',
    #                             samesite='None'  # This is the key part for cross-site requests

    #                             # domain="frontend.com"
    #                             )
    #                     return resp
    #                 except Exception as e:
    #                     return {
    #                         "error": "Something went wrong",
    #                         "message": str(e)
    #                     }, 500
    #             return {
    #                 "message": "Error fetching auth token!",
    #                 "data": None,
    #                 "error": "Unauthorized"
    #             }, 404
    #         except Exception as e:
    #             return {
    #                     "message": "Something went wrong!",
    #                     "error": str(e),
    #                     "data": None
    #             }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    #api.add_resource(_Security, '/authenticate')
    
    