import datetime
from flask import request, jsonify, g
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import text
from .models import Task
from flask_restful import Resource, reqparse
from app import db, ma


class TasksSchema(ma.Schema):
    class Meta:
        fields = ("id", "state", "subject", "text", "create_date", "done_date")


parser = reqparse.RequestParser()
task_schema = TasksSchema()
tasks_schema = TasksSchema(many=True)


class Todo(Resource):

	@login_required
	def get(self, todo_id):
		if todo_id:
			owner_id = current_user.id
			res = Task.query.filter_by(id=todo_id, owner=owner_id).first()
			task = task_schema.dump(res)
			if task != {}:
				return {'data': task}, 200
			else:
				return {'data': f"Task {todo_id} not exists"}, 404
		else:
			return {'data': 'Task id not exists'}, 404


	@login_required
	def post(self):
		parser.add_argument('new_task_subject', location=['values', 'form'])
		parser.add_argument('new_task_text', location=['values', 'form'])
		params = parser.parse_args()

		new_task = Task(owner=current_user.id, state="todo",
						subject=params.get('new_task_subject'),
						text=params.get('new_task_text'))
		db.session.add(new_task)
		db.session.commit()
		return task_schema.dump(new_task), 201


	@login_required
	def put(self, todo_id):
		parser.add_argument('todo_id', location=['values', 'form'])
		parser.add_argument('state', location=['values', 'form'])
		parser.add_argument('subject', location=['values', 'form'])
		parser.add_argument('text', location=['values', 'form'])
		params = parser.parse_args()
		id = params.get('todo_id')

		task = Task.query.get(todo_id)
		current_task_state = task.state
		if task and task.owner == current_user.id:
			print(f' task {task} {task.owner} {current_user.id}')
			for key, value in params.items():
				if key == 'todo_id':
					continue

				if key == 'state' and value is not None and value != current_task_state:
					if current_task_state == 'todo' and value == 'done':
						task.state = value
						task.done_date = str(datetime.datetime.utcnow())
					else:
						task.state = value
						task.done_date = None

				if key != 'state' and value is not None and value != task.__dict__.get(key):
					setattr(task, key, value)

			db.session.add(task)
			db.session.commit()
			return task_schema.dump(task), 201

		return {'data': 'Access denied'}, 403


	@login_required
	def delete(self, todo_id):

		task = Task.query.get(todo_id)
		if task and task.owner == current_user.id:
			db.session.delete(task)
			db.session.commit()
			return {'data': f" Task {todo_id} deleted"}, 200

		return {'data': 'Access denied'}, 403


class AllTasksView(Resource):

	@login_required
	def get(self):
		tasks = Task.query.filter_by(owner=current_user.id)
		print(task_schema.dump(tasks))
		return {"todos": tasks_schema.dump(tasks)}




