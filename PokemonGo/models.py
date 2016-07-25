from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))
	name = db.Column(db.String(80))
	phone = db.Column(db.BigInteger)
	team = db.Column(db.Integer)
	device_token = db.Column(db.String(80))

	def __init__(self, username, password, name, phone, team, device_token=""):
		self.username = username
		self.password = password
		self.name = name
		self.phone = phone
		self.team = team
		self.device_token = ""

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'username' : self.username,
			'password' : self.password,
			'name' : self.name,
			'phone' : self.phone,
			'team' : self.team,
			'device_token' : self.device_token
		}

	def insert_into_db(self):
		user = User.query.filter_by(username=self.username).first()
		if user is None:
			db.session.add(self)
			db.session.commit()
			return self.serialize

	def update_device_token(self, device_token):
		self.device_token = device_token
		db.session.commit()

class Reports(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.BigInteger)
	latitude = db.Column(db.Float(precision=64))
	longitude = db.Column(db.Float(precision=64))
	pokemon = db.Column(db.Integer)
	user = db.Column(db.Integer)

	def __init__(self, latitude, longitude, pokemon, user_id=-1):
		self.timestamp = time.time()
		self.latitude = latitude
		self.longitude = longitude
		self.pokemon = pokemon
		self.user = user_id

	@property
	def serialize(self):
		serial = {
			'id' : self.id,
			'timestamp' : self.timestamp,
			'latitude' : self.latitude,
			'longitude' : self.longitude,
			'pokemon' : self.pokemon,
			'user' : None
		}
		user = User.query.filter_by(id=self.user).first()
		if user is not None:
			serial['user'] = user.serialize
		return serial

	def insert_into_db(self):
		db.session.add(self)
		db.session.commit()
		return self.id

class Notifications(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer)
	pokemon = db.Column(db.Integer)
	status = db.Column(db.Integer)

	def __init__(self, user, pokemon):
		self.user = user
		self.pokemon = pokemon
		self.status = 0

	@property 
	def serialize(self):
		return {
			'id' : self.id,
			'user' : User.query.filter_by(id=self.user).first().serialize,
			'pokemon' : self.pokemon,
			'status' : self.status
		}

	def delete(self):
		self.status = 1
		db.session.commit()
		return self.serialize

	def insert_into_db(self):
		notification = Notifications.query.filter_by(user=self.user).filter_by(pokemon=self.pokemon).first()
		if notification is None:
			db.session.add(self)
			db.session.commit()
			return self.serialize
		else:
			notification.status = 0
			db.session.commit()
			return notification.serialize

	@staticmethod
	def get_users_notifs(id):
		return [notification.serialize for notification in Notifications.query.filter_by(user=id).all()]






