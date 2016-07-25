from flask import request, jsonify
from models import Notifications, Reports, User, db
import time
import random
from apns import APNs, Frame, Payload
import os 

pokemonList = ["bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard", "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree", "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot", "rattata", "raticate", "spearow", "fearow", "ekans", "arbok", "pikachu", "raichu", "sandshrew", "sandslash", "nidoran-f", "nidorina", "nidoqueen", "nidoran-m", "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales", "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish", "gloom", "vileplume", "paras", "parasect", "venonat", "venomoth", "diglett", "dugtrio", "meowth", "persian", "psyduck", "golduck", "mankey", "primeape", "growlithe", "arcanine", "poliwag", "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop", "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool", "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke", "magnemite", "magneton", "farfetchd", "doduo", "dodrio", "seel", "dewgong", "grimer", "muk", "shellder", "cloyster", "gastly", "haunter", "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb", "electrode", "exeggcute", "exeggutor", "cubone", "marowak", "hitmonlee", "hitmonchan", "lickitung", "koffing", "weezing", "rhyhorn", "rhydon", "chansey", "tangela", "kangaskhan", "horsea", "seadra", "goldeen", "seaking", "staryu", "starmie", "mr-mime", "scyther", "jynx", "electabuzz", "magmar", "pinsir", "tauros", "magikarp", "gyarados", "lapras", "ditto", "eevee", "vaporeon", "jolteon", "flareon", "porygon", "omanyte", "omastar", "kabuto", "kabutops", "aerodactyl", "snorlax", "articuno","zapdos", "moltres", "dratini", "dragonair", "dragonite", "mewtwo", "mew"]

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
		pokemon_name_list = []
		for notification in notifications:
			print('notifications')
			pokemon = notification.pokemon
			print(pokemon)
			report = Reports.query.filter(Reports.latitude <= latitude  + block_dim ).filter(Reports.latitude >= latitude - block_dim).filter(Reports.longitude >= longitude - block_dim).filter(Reports.longitude <= longitude + block_dim).filter(Reports.pokemon == pokemon).first()
			if report is not None:
				pokemon_name_list.append(pokemonList[int(notification.pokemon)])
			if len(pokemon_name_list) > 3:
				pokemon_name_list.append("and more")
				break
		if len(pokemon_name_list) > 0:
			pokemon_name_list = str(pokemon_name_list).strip('[]').replace("'", "")
			print(user.device_token)
			send_APN(curr_dir + "/pushcert.pem", user.device_token, pokemon_name_list)
		print(pokemon_name_list)
		return jsonify(success=0)
	return jsonify(success=1)

def response_listener(error_response):
	print(error_response)

def send_APN(directory, device_token, pokemon):
	apns = APNs(use_sandbox = True, cert_file=directory, enhanced=True)
	identifier = random.getrandbits(32)
	token_hex = device_token
	payload = Payload(alert=pokemon + " was found near you!", sound="default", badge=1)
	apns.gateway_server.register_response_listener(response_listener)
	apns.gateway_server.send_notification(token_hex, payload, identifier=identifier)

def add_device_token():
	device_token = request.args.get('dt')
	user = request.args.get('user')
	if device_token is not None and user is not None:
		user = User.query.filter_by(id=user).first()
		user.update_device_token(device_token)
		return jsonify(success=0)
	return jsonify(success=1, error='check args')


