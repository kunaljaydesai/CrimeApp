from flask import request, jsonify
from models import Notifications, Reports, User
from views.api_wrappers.twilio_client import TwilioClient

def add_notification():
	user = request.args.get('user')
	pokemon = request.args.get('pokemon')
	if user is not None and pokemon is not None:
		notification = Notifications(user, pokemon)
		notif = notification.insert_into_db()
		return jsonify(success=0, notification=notif)
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
	if user is not None and latitude is not None and longitude is not None:
		user = User.query.filter_by(id=user).first()
		notifications = Notifications.query.filter_by(user=user).filter_by(status=0).all()
		for notification in notifications:
			pokemon = notification.pokemon
			report = Reports.query.filter(Reports.latitude > latitude + block_dim).filter(Reports.latitude < latitude - block_dim).filter(Reports.longitude > longitude - block_dim).filter(Reports.longitude < longitude + block_dim).filter(Reports.pokemon == pokemon).first()
			if report is not None:
				TwilioClient.send_message_to(pokemon=pokemon, latitude=latitude, longitude=longitude, to=user.phone)
		return jsonify(success=0)
	return jsonify(success=1)
