from flask import Flask, jsonify, request, session, redirect, url_for
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from config import app, db

migrate = Migrate(app, db) 


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app, resources={r"/*": {"origins": "https://example.com"}})

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify(users)

class TeacherResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        return jsonify(teachers)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({"message": "Login successful!", "user_id": user.id, "role": user.role})
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login required"}), 401


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users)

@app.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    return jsonify(teachers)

if __name__ == '__main__':
    db.create_all() 
    app.run(port=5555)
