from flask import request, jsonify
from models import Notifications, Reports, User, db
import time
import random
from apns import APNs, Frame, Payload
import os 

def add_notification():
	user = request.args.get('user')
	pokemon = request.args.get('pokemon')
	if user is not None and pokemon is not None:
		notification = Notifications(user, pokemon)
		notif = notification.insert_into_db()
		return jsonify(success=0, notification=notif)
	return jsonify(success=1, error='check args')

def delete_notification():
	user = request.args.get('user')
	pokemon = request.args.get('pokemon')
	if user is not None and pokemon is not None:
		Notifications.query.filter_by(user=user, pokemon=pokemon).delete()
		db.session.commit()
		return jsonify(success=0)
	return jsonify(success=1, error='check args')

def get_notification():
	user = request.args.get('user')
	if user is not None:
		return jsonify(success=0, notifications=Notifications.get_users_notifs(float(user)))
	return jsonify(success=1, error='check args')

def send_notification():
	user = request.args.get('user')
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')
	block_dim = 0.00027472527473
	curr_dir = os.path.dirname(os.path.realpath(__file__))
	if user is not None and latitude is not None and longitude is not None:
		user = User.query.filter_by(id=user).first()
		notifications = Notifications.query.filter_by(user=user.id).all()
		latitude = float(latitude)
		longitude = float(longitude)
		for notification in notifications:
			print('notifications')
			pokemon = notification.pokemon
			print(pokemon)
			report = Reports.query.filter(Reports.latitude <= latitude  + block_dim ).filter(Reports.latitude >= latitude - block_dim).filter(Reports.longitude >= longitude - block_dim).filter(Reports.longitude <= longitude + block_dim).filter(Reports.pokemon == pokemon).first()
			if report is not None:
				print('there is a report')
				send_APN(curr_dir + "/pushcert.pem", '3aba425abe4476b2fa5ceec8f45887e0139d5a357a63d190f8670e1ffd618155')
		return jsonify(success=0)
	return jsonify(success=1)

def response_listener(error_response):
	print(error_response)

def send_APN(directory, device_token):
	apns = APNs(use_sandbox = True, cert_file=directory, enhanced=True)
	identifier = random.getrandbits(32)
	token_hex = device_token
	payload = Payload(alert="pushcert.pem", sound="default", badge=1)
	apns.gateway_server.register_response_listener(response_listener)
	apns.gateway_server.send_notification(token_hex, payload, identifier=identifier)


