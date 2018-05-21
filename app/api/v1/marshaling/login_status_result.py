from flask_restful import fields

login_status_result = {
    'userId': fields.String(),
    'token': fields.String()
}
