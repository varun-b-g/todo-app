'''Todo api'''
import logging
from flask import Flask, render_template, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from cerberus import Validator
from errors import bad_request, not_found, method_not_allowed, unsupported_media_type, internal_server_error

app = Flask(__name__, static_folder='../frontend/dist/static', template_folder='../frontend/dist')

app.config.from_json('./flask_config.json')

db = SQLAlchemy(app)


class Todo(db.Model):
  '''Todo model containing id and title'''
  __tablename__ = 'todo'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.Text())

  def __init__(self, id, title):
    self.id = id
    self.title = title


error_handlers = [(400, bad_request), (404, not_found), (405, method_not_allowed), (415, unsupported_media_type), (500, internal_server_error), (Exception, internal_server_error)]
for status_code, error_handler in error_handlers:
  app.register_error_handler(status_code, error_handler)


@app.teardown_appcontext
def close_session(error):
  if error and db.session.is_active:
    db.session.rollback()
  else:
    db.session.commit()

  db.session.close()


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
def index(path):
  '''Todo app'''
  return render_template('index.html')


@app.route('/api/create_todo', methods=['POST'])
def create_todo():
  '''Todo creation'''
  content_type = request.headers.get('Content-Type')
  if content_type is None or content_type != 'application/json':
    abort(415)

  parameters = request.get_json(silent=True)
  if not isinstance(parameters, dict) or not Validator(app.config['TODO_VALIDATION_SCHEMA'])(parameters):
    abort(400)

  try:
    db.session.add(Todo(id=parameters['id'], title=parameters['title']))
    db.session.commit()
  except Exception as e:
    logging.error(e)
    abort(500)

  return jsonify({'id': parameters['id']})


@app.route('/api/delete_todo', methods=['DELETE'])
def delete_todo():
  '''Todo deletion'''
  content_type = request.headers.get('Content-Type')
  if content_type is None or content_type != 'application/json':
    abort(415)

  parameters = request.get_json(silent=True)
  if not isinstance(parameters, dict) or not Validator(app.config['ID_VALIDATION_SCHEMA'])(parameters):
    abort(400)

  try:
    todo_to_delete = db.session.query(Todo).filter(Todo.id == parameters['id']).first()
    db.session.delete(todo_to_delete)
    db.session.commit()
  except Exception as e:
    logging.error(e)
    abort(500)

  return jsonify({'id': parameters['id']})


@app.route('/api/get_all_todo', methods=['GET'])
def get_all_todo():
  '''All todo getting'''
  try:
    all_todos = [{'id': todo.id, 'title': todo.title} for todo in db.session.query(Todo).all()]
  except Exception as e:
    logging.error(e)
    abort(500)

  return jsonify(all_todos)
