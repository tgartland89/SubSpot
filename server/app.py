from flask import Flask, jsonify, request, make_response, render_template, session
from flask_restful import Resource, fields, marshal 
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from config import app, db, api
from flask_cors import CORS

CORS(app, supports_credentials=True)
app.template_folder = "templates"

user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'password_hash': fields.String,
    'profile_picture': fields.String,
    'role': fields.String,
}

teacher_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'school': fields.String,
    'location': fields.String,
    'grade_or_course': fields.String,
    'image_url': fields.String,
}

substitute_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'verification_id': fields.String,
    'location': fields.String,
    'grade_or_course': fields.String,
    'qualifications': fields.String,
    'image_url': fields.String,
}

site_admin_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'name': fields.String,
    'image_url': fields.String,
}

course_fields = {
    'id': fields.Integer,
    'teacher_id': fields.Integer,
    'substitute_id': fields.Integer,
    'class_subject': fields.String,
    'date': fields.String,
    'time': fields.String,
    'status': fields.String,
}
review_fields = {
    'id': fields.Integer,
    'teacher_id': fields.Integer,
    'substitute_id': fields.Integer,
    'rating': fields.Float,
    'comment': fields.String,
}

class SignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
       
            user = User(
                email=data['email'],
                password=data['password'], 
                role='Teacher',
            )
            db.session.add(user)
            db.session.commit()

            user_id =user.id

            teacher = Teacher(
                user_id=user.id,  
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                school=data['school'],
                location=data['location'],
                grade_or_course=data['grade_or_course'],
            )
            db.session.add(teacher)
            db.session.commit()

            return make_response({'message': 'New teacher created successfully'}, 201)
        except Exception as e:
            print(e) 
            return make_response({'errors': ['Validation errors']}, 400)
        
class SubstituteSignUp(Resource):
    def post(self):
        try:
            data = request.get_json()
       

            user = User(
                email=data['email'],
                password=data['password'], 
                role='Substitute',
            )
      
            db.session.add(user)
            db.session.commit()

      
            user_id = user.id


            substitute = Substitute(
                user_id=user_id,  
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                location=data['location'],
                grade_or_course=data['grade_or_course'],
                verification_id=data['verification_id'],
                qualifications=data['qualifications'],
            )
   
            db.session.add(substitute)
            db.session.commit()

            return make_response({'message': 'New substitute created successfully'}, 201)
        except Exception as e:
            print(e) 
            return make_response({'errors': ['Validation errors']}, 400)

        
class LogIn(Resource):
    def post(self):
        data = request.get_json()
        # Your logic for authenticating the user login credentials goes here
        email = data.get('email')
        password = data.get('password')
        teacher = Teacher.query.filter_by(email=email).first()

        if teacher and teacher.password_hash == password:  # In real-world, use proper password hashing
            session['user_id'] = teacher.id
            return make_response({'message': 'Login successful'}, 201)
        else:
            return make_response({'errors': ['Invalid credentials']}, 401)

class LogOut(Resource):
    def delete(self):
        # Your logic for logging out the user (clearing the session) goes here
        session.pop('user_id', None)  # Clear the user_id from the session
        return make_response({'message': 'Logged out successfully'}, 204)


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        serialized_users = [marshal(user, user_fields) for user in users]
        return jsonify(serialized_users)

class TeacherResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        # Use marshal to serialize the Teacher objects
        serialized_teachers = [marshal(teacher, teacher_fields) for teacher in teachers]
        return jsonify(serialized_teachers)

class SubstituteResource(Resource):
    def get(self):
        substitutes = Substitute.query.all()
        serialized_substitutes = [marshal(substitute, substitute_fields) for substitute in substitutes]
        return jsonify(serialized_substitutes)

class SiteAdminResource(Resource):
    def get(self):
        site_admins = SiteAdmin.query.all()
        serialized_site_admins = [marshal(admin, site_admin_fields) for admin in site_admins]
        return jsonify(serialized_site_admins)

class CourseResource(Resource):
    def get(self):
        courses = Course.query.all()
        serialized_courses = [marshal(course, course_fields) for course in courses]
        return jsonify(serialized_courses)

class ReviewResource(Resource):
    def get(self):
        reviews = Review.query.all()
        serialized_reviews = [marshal(review, review_fields) for review in reviews]
        return jsonify(serialized_reviews)
    
api.add_resource(SignUp, '/signup')
api.add_resource(LogIn, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(UserResource, '/users')
api.add_resource(TeacherResource, '/teachers')
api.add_resource(SubstituteResource, '/substitutes')
api.add_resource(SiteAdminResource, '/site_admins')
api.add_resource(CourseResource, '/courses')
api.add_resource(ReviewResource, '/reviews')
api.add_resource(SubstituteSignUp, '/substitute-signup')


# Route for teacher form
@app.route('/teacher-form', methods=['GET', 'POST'])
def teacher_form():
    if request.method == 'POST':
        # Get form data and create a new Teacher record in the database
        data = request.form
        teacher = Teacher(
            name=data['name'],
            school=data['school'],
            location=data['location'],
            grade_or_course=data['grade_or_course'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(teacher)
        db.session.commit()
        return make_response({'message': 'Teacher added successfully'}, 201)
    return render_template('teacher_form.html')

# Route for substitute form
@app.route('/substitute-form', methods=['GET', 'POST'])
def substitute_form():
    if request.method == 'POST':
        # Get form data and create a new Substitute record in the database
        data = request.form
        substitute = Substitute(
            name=data['name'],
            verification_id=data['verification_id'],
            location=data['location'],
            grade_or_course=data['grade_or_course'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(substitute)
        db.session.commit()
        return make_response({'message': 'Substitute added successfully'}, 201)
    return render_template('substitute_form.html')

if __name__ == '__main__':
    app.run(port=5555)
