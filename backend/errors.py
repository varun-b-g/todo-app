'''Error handlers'''
import logging
from flask import Blueprint, jsonify, make_response

app = Blueprint('errors', __name__)


def bad_request(error):
  '''Handle invalid json was requested.'''
  logging.warning(error)
  return make_response(jsonify({'message': 'Requested json is invalid.'}), 400)


def not_found(error):
  '''Handle not found.'''
  return make_response({'message': 'Resource not found'}, 404)


def method_not_allowed(error):
  '''Handle prohibited request method was requested.'''
  logging.warning(error)
  response = make_response(jsonify({'message': 'Requested method is not allowed.'}), 405)
  response.headers['Allow'] = error.valid_methods
  return response


def unsupported_media_type(error):
  '''Handle unsupported media type.'''
  logging.warning(error)
  return make_response(jsonify({'message': 'Requested Content-Type is unsupported.'}), 415)


def internal_server_error(error):
  '''Handle internal server error.'''
  logging.error(error)
  return make_response(jsonify({'message': 'Internal server error occurred.'}), 500)
