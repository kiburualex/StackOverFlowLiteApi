from app.modules.user.models import User, Token


class Auth:

    @staticmethod
    def login_user(data):
        try:

            """ Get the User by email """

            user = User({"email": data.get('email')}).filter_by_email()
            if user and User().check_password(data.get('email'), data.get('password')):

                """ Encode token for the user using email details """

                auth_token = User().encode_auth_token(data.get('email'))

                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):

        if data:

            """
                Separates by white space and takes the token only
            """
            auth_token = data.split(" ")[1]

        else:

            auth_token = ''

        if auth_token:

            resp = User().decode_auth_token(auth_token)

            if not isinstance(resp, str):

                """ Mark the token as black-listed """

                Token().save(auth_token)
                response_object = {
                    'status': 'success',
                    'message': 'logged out'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):

        """ Get authentication token via request """

        auth_token = new_request.headers.get('Authorization')

        if auth_token:

            """ Decode to get the id (should be int)"""
            resp = User().decode_auth_token(auth_token)

            if not isinstance(resp, str):

                """ Get user by decoded id """
                user = User({"id": resp}).get_by_id()

                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.get('id'),
                        'email': user.get('email'),
                        'username': user.get('username')
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401