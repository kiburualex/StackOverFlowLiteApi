from flask import jsonify, Blueprint
from flask_restplus import Resource, Api

api = Api(version='1.0', title='StackOverflow Lite API',
          description='Flask RestPlus API version 1 for the StackOverflow lite application')