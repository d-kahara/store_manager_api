import re
from .user_model import User
# from ..service.blacklist_service import save_token


class Auth:


    @staticmethod
    def logout_user(data):
        if data:
            token = data.split(" ")[1]
        else:
            token = ''
        if token:
            resp = User.decode_jwt_token(token)
            #print(resp)
            if not isinstance(resp, int):
                # to-do mark the token as blacklisted in datastore
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }

                return response_object, 200
            else:
                response_object = {
                    'status': 'Failed',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'failed',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    # @staticmethod
    # def get_current_user(new_request):
    #         # get the auth token
    #         auth_token = new_request.headers.get('Authorization')
    #         if auth_token:
    #             resp = User.decode_auth_token(auth_token)
    #             if not isinstance(resp, str):
    #                 user = User.query.filter_by(id=resp).first()
    #                 response_object = {
    #                     'status': 'success',
    #                     'data': {
    #                         'user_id': user.id,
    #                         'email': user.email,
    #                         'admin': user.admin,
    #                         'registered_on': str(user.registered_on)
    #                     }
    #                 }
    #                 return response_object, 200
    #             response_object = {
    #                 'status': 'fail',
    #                 'message': resp
    #             }
    #             return response_object, 401
    #         else:
    #             response_object = {
    #                 'status': 'fail',
    #                 'message': 'Provide a valid auth token.'
    #             }
    #             return response_object, 401
