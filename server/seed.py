import os
from faker import Faker
from app import app, db, bcrypt, User, Teacher, Substitute
from models import Review, Request

fake = Faker()

def create_fake_admin():
    email = 'C.Chase@sample.com'
    password = 'Disney4Life!'
    name = 'Colleen Chase'
    location = 'Aurora, CO'
    phone = '303-867-5309'
    existing_admin = User.query.filter_by(email=email).first()

    if not existing_admin:
        admin = User(name=name, email=email, location=location, phone=phone, role='SiteAdmin')
        admin.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  
        db.session.add(admin)
        db.session.commit()

        print("Fake admin 'Colleen Chase' created successfully.")

def create_fake_teachers(count=5):
    for _ in range(count):
        name = fake.name()
        email = fake.email()
        location = fake.city()
        phone = fake.phone_number()
        school_name = fake.company()
        school_location = fake.city()
        course_name = fake.random_element(['Math', 'Science', 'History', 'English'])
        password = 'password'  

        user = User(name=name, email=email, location=location, phone=phone, role='Teacher')
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  
        db.session.add(user)
        db.session.commit()

        teacher = Teacher(user=user, name=name, email=email, location=location, phone=phone,
                          school_name=school_name, school_location=school_location, course_name=course_name)
        db.session.add(teacher)
        db.session.commit()

def create_fake_substitutes(count=5):
    for _ in range(count):
        name = fake.name()
        email = fake.email()
        location = fake.city()
        phone = fake.phone_number()
        qualifications = fake.sentence(nb_words=6)
        verification_id = fake.random_int(min=1000, max=9999)
        password = 'password'  

        user = User(name=name, email=email, location=location, phone=phone, role='Substitute')
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')  
        db.session.add(user)
        db.session.commit()

        substitute = Substitute(user=user, name=name, email=email, location=location, phone=phone,
                                qualifications=qualifications, verification_id=verification_id)
        db.session.add(substitute)
        db.session.commit()

def create_fake_requests(count=20):
    teachers = Teacher.query.all()
    substitutes = Substitute.query.all()

    for _ in range(count):
        teacher = fake.random_element(teachers)
        substitute = fake.random_element(substitutes)
        course_being_covered = fake.random_element(['Math', 'Science', 'History', 'English'])
        confirmation = fake.boolean()
        message_sub_sent_to = fake.sentence()
        teacher_if_declined = fake.boolean()
        school_name = fake.company()
        teacher_school_location = fake.city()

        request = Request(substitute_user_id=substitute.user.id, teacher_user_id=teacher.user.id,
                          course_being_covered=course_being_covered, confirmation=confirmation,
                          message_sub_sent_to=message_sub_sent_to, teacher_if_declined=teacher_if_declined,
                          school_name=school_name, teacher_school_location=teacher_school_location)
        db.session.add(request)
        db.session.commit()

def create_fake_reviews(count=10):
    teachers = Teacher.query.all()
    substitutes = Substitute.query.all()

    for _ in range(count):
        reviewer_teacher = fake.random_element(teachers)
        substitute = fake.random_element(substitutes)
        rating = fake.random_int(min=1, max=5)
        comment = fake.paragraph()

        review = Review(reviewer_teacher_id=reviewer_teacher.id, substitute_id=substitute.id,
                        rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
        
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        create_fake_admin()
        create_fake_teachers()
        create_fake_substitutes()
        create_fake_reviews()
        create_fake_requests()

        print("Fake data generated successfully.")