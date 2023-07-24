from flask import Flask, jsonify, request, make_response, session
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_cors import CORS
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from config import app, db


migrate = Migrate(app, db)

CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

migrate = Migrate(app, db)

CORS(app)  


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify(users)

@app.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()

    return jsonify(teachers)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
