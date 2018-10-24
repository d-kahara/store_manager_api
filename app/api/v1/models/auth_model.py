import re
from .user_model import User
# from ..service.blacklist_service import save_token


class Auth:


    @staticmethod
    def logout_user(data):
        """This methods logs out the current user"""
        if data:
            token = data.split(" ")[1]
        else:
            token = ''
        if token:
            resp = User.decode_jwt_token(token)
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

  