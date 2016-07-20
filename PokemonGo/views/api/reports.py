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

def get_reports_filter():
	tl_lat = float(request.args.get('top_left_latitude'))
	tl_lon = float(request.args.get('top_left_longitude'))
	br_lat = float(request.args.get('bottom_right_latitude'))
	br_lon = float(request.args.get('bottom_right_longitude'))
	below_tl = Reports.query.filter(tl_lat >= Reports.latitude)
	above_br = below_tl.filter(br_lat <= Reports.latitude)
	left_br = above_br.filter(br_lon >= Reports.longitude)
	right_tl = left_br.filter(tl_lon <= Reports.longitude)
	list_of_reports = right_tl.all()
	return jsonify(success=0, reports=[report.serialize for report in list_of_reports])
