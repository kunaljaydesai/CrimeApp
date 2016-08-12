from flask import request, jsonify	
from models import Reports, User, Notifications, Vote
import random
from apns import APNs, Frame, Payload
import os

pokemonList = ["bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard", "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree", "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot", "rattata", "raticate", "spearow", "fearow", "ekans", "arbok", "pikachu", "raichu", "sandshrew", "sandslash", "nidoran-f", "nidorina", "nidoqueen", "nidoran-m", "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales", "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish", "gloom", "vileplume", "paras", "parasect", "venonat", "venomoth", "diglett", "dugtrio", "meowth", "persian", "psyduck", "golduck", "mankey", "primeape", "growlithe", "arcanine", "poliwag", "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop", "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool", "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke", "magnemite", "magneton", "farfetchd", "doduo", "dodrio", "seel", "dewgong", "grimer", "muk", "shellder", "cloyster", "gastly", "haunter", "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb", "electrode", "exeggcute", "exeggutor", "cubone", "marowak", "hitmonlee", "hitmonchan", "lickitung", "koffing", "weezing", "rhyhorn", "rhydon", "chansey", "tangela", "kangaskhan", "horsea", "seadra", "goldeen", "seaking", "staryu", "starmie", "mr-mime", "scyther", "jynx", "electabuzz", "magmar", "pinsir", "tauros", "magikarp", "gyarados", "lapras", "ditto", "eevee", "vaporeon", "jolteon", "flareon", "porygon", "omanyte", "omastar", "kabuto", "kabutops", "aerodactyl", "snorlax", "articuno","zapdos", "moltres", "dratini", "dragonair", "dragonite", "mewtwo", "mew"]


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
		block_dim = 0.01
		users_in_radius = User.query.filter(User.latitude <= latitude  + block_dim ).filter(User.latitude >= latitude - block_dim).filter(User.longitude >= longitude - block_dim).filter(User.longitude <= longitude + block_dim).all()
		for user in users_in_radius:
			print(str(user.username) + " is in radius.")
			notification = Notifications.query.filter_by(user=user.id, pokemon=pokemon).first()
			if notification is not None:
				curr_dir = os.path.dirname(os.path.realpath(__file__)) + "/pushcert.pem"
				send_APN(curr_dir, user.device_token, pokemonList[int(pokemon)] + " was reported near you!")
		return jsonify(success=0, report=report.serialize)
	return jsonify(success=1, error='check request params')

def get_reports():
	id = request.args.get('id')
	user_id = request.args.get('user_id')
	try:
		if id is None:
			list_of_reports = Reports.query.all()
			return jsonify(success=0, reports=[report.serialize for report in list_of_reports])
		elif id is not None and user_id is not None:
			report = Reports.query.filter_by(id=id).first()
			serialized_report = report.serialize
			vote = Vote.query.filter_by(user=user_id, report=report.id).first()
			print(vote)
			if vote is not None:
				serialized_report['voted'] = vote.type_vote
			else:
				serialized_report['voted'] = 0
			return jsonify(success=0, report=serialized_report)
		else:
			return jsonify(success=1, error='database issue')
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

def response_listener(error_response):
	print(error_response)

def send_APN(directory, device_token, pokemon):
	apns = APNs(use_sandbox = True, cert_file=directory, enhanced=True)
	identifier = random.getrandbits(32)
	token_hex = device_token
	payload = Payload(alert=pokemon, sound="default", badge=1)
	apns.gateway_server.register_response_listener(response_listener)
	apns.gateway_server.send_notification(token_hex, payload, identifier=identifier)

def upvote():
	id = request.args.get('id')
	user_id = request.args.get('user_id')
	report = Reports.query.filter_by(id=id).first()
	Vote(user_id, report.id, type_vote=1).insert_into_db()
	if report is not None:
		report.up_vote()
	return jsonify(success=0)

def downvote():
	id = request.args.get('id')
	user_id = request.args.get('user_id')
	report = Reports.query.filter_by(id=id).first()
	Vote(user_id, report.id, type_vote=2).insert_into_db()
	if report is not None:
		report.down_vote()
	return jsonify(success=0)