from flask import Flask, request, render_template, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db, Reports
from views.api import reports, users, notifications
import requests

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:crimeapp@crime.cnfegalrlacy.us-west-2.rds.amazonaws.com/pokemongo'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(application)

@application.before_first_request
def create_tables():
	print('creating tables')
	db.create_all()
	db.session.commit()
	print('created tables')

###API

#reports

application.add_url_rule('/api/reports/add', view_func=reports.add_report)
application.add_url_rule('/api/reports/get', view_func=reports.get_reports)

#users

application.add_url_rule('/api/users/add', view_func=users.add_user)
application.add_url_rule('/api/users/authenticate', view_func=users.authenticate_user)

#notifications

application.add_url_rule('/api/notifications/add', view_func=notifications.add_notification)
application.add_url_rule('/api/notifications/get', view_func=notifications.get_notification)
application.add_url_rule('/api/notifications/send', view_func=notifications.send_notification)

if __name__ == "__main__":
	application.run(host="0.0.0.0", port=80, debug=True)