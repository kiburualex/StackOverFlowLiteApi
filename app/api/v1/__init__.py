from flask_restplus import Api

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(version='1.0', title='StackOverflow Lite API',
          description='Flask RestPlus API version 1 for the StackOverflow lite application')
