from app import api_root
from flask_restful import Resource, marshal_with
from flask import request
from app.model.User import User
from app.model.Token import Token
from app.api.v1.marshaling.login_status_result import login_status_result
from app import db
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
import hashlib


@api_root.resource("/v1/login")
class Login(Resource):

    @marshal_with(login_status_result)
    def post(self):
        try:

            json_data = request.get_json(force=True)
            username = json_data['username']
            password = json_data['password']

            try:

                user = User.query.filter(User.username == username).one()


            except NoResultFound:

                print("아이디가 없음 " + username)
                return None, 401

            join_date = str(user.joinDate.strftime("%y/%m/%d"))
            password_hashSHA = hashlib.sha256()
            password_hashSHA.update((password + join_date).encode('utf-8'))
            password = password_hashSHA.hexdigest()

            # user = User(username=username, password=password, joinDate=join_date)

            if user.password != password:
                return None, 401
            else:
                now = datetime.now()

                due_date = str(now + timedelta(hours=3))
                due_date_hashSHA = hashlib.sha256()
                due_date_hashSHA.update(due_date.encode('utf-8'))
                hash_date = due_date_hashSHA.hexdigest()

                token = Token(token=hash_date, dueDate=due_date, userId=user.id)

                db.session.add(token)
                db.session.commit()

                return token


        except Exception:

            return None, 400