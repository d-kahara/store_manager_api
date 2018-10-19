from .user_model import User
# from ..service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        #fetch the user data
        try:
            email = data.get('email')
            password = data.get('password')
            user = User.find_user_by_email()               
            if user and user.validate_user_password(password):
                token = user.encode_auth_token(email)
                if token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully Logged In',
                        'Authorization': token.decode()
                    }
                    return response_object, 200

        except Exception as e:
            print(e)
            response_object = {
                'status': 'Request failed ',
                'message': 'Please try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        if data:
            token = data.split(" ")[1]
        else:
            token = ''
        if token:
            resp = User.decode_jwt_token(token)
            if not isinstance(resp, str):
                # to-do mark the token as blacklisted in datastore
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }

                return response_object, 200
            else:
                response_object = {
                    'status': 'failed',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

