from flask import request, jsonify
from models import User

def add_user():
	username = request.args.get('username')
	password = request.args.get('password')
	name = request.args.get('name')
	phone = request.args.get('phone')
	team = request.args.get('team')
	if username is not None and password is not None and name is not None and phone is not None and team is not None:
		user = User(username, password, name, phone, team)
		user.insert_into_db()
		if user is not None:
			return jsonify(success=1, user=user.serialize)
		else:
			return jsonify(success=0, error='username exists')
	return jsonify(success=0, error='check arguments')

def authenticate_user():
	try:
		username = request.args.get('username')
		password = request.args.get('password')
		user = User.query.filter_by(username=username, password=password).first()
		if user is not None:
			return jsonify(success=0, user=user.serialize)
		return jsonify(success=1, error='Authenication error')
	except:
		return jsonify(success=1, error='Server is down')