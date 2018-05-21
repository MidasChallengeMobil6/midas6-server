from app import api_root
from flask_restful import Resource
from flask import request
from jsonschema import validate
from app.model.User import User
from app import db
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
import hashlib


@api_root.resource("/v1/signup")
class SignUp(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "username" : {"type": "string"},
                "email" : {"type": "string"},
                "password" : {"type": "string"}
            }
        }

        validate(json_data, schema)

        name = json_data['name']
        username = json_data['username']
        email = json_data['email']
        password = json_data['password']


        # 동일한 아이디가 있으면 에러코드 1 : 실패
        # 에러코드 0 : 성공

        try:
            user = User.query.filter(User.username == username).one()
        except NoResultFound as e:

            join_date = datetime.now().strftime("%y/%m/%d")
            join_date = str(join_date)

            password_hashSHA = hashlib.sha256()
            password_hashSHA.update((password + join_date).encode('utf-8'))
            password = password_hashSHA.hexdigest()

            user = User(name=name, username=username, email=email, password=password, joinDate=join_date)

            db.session.add(user)
            db.session.commit()

            print("회원가입 성공: " + username)

            response = {
                "err": 0,
                "data": {}
            }

            return response

        print("회원가입 불가능 - 동일한 아이디 : " + username)
        response = {
            "err": 1,
            "data": {}
        }
        return response



