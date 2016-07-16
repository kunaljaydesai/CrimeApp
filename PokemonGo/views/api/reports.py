from flask import request, jsonify	
from models import Reports

def add_report():
	pokemon = request.args.get('pokemon')
	latitude = request.args.get('latitude')
	longitude = request.args.get('longitude')
	user_id = request.args.get('user_id')
	if pokemon is not None and latitude is not None and longitude is not None:
		pokemon = float(pokemon)
		latitude = float(latitude)
		longitude = float(longitude)
		report = Reports(latitude, longitude, pokemon, user_id=user_id)
		id = report.insert_into_db()
		return jsonify(success=0, report=report.serialize)
	return jsonify(success=1, error='check request params')

def get_reports():
	try:
		list_of_reports = Reports.query.all()
		return jsonify(success=0, reports=[report.serialize for report in list_of_reports])
	except:
		return jsonify(success=1, error='database issue')
