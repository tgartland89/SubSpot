from flask import Flask
from config import app, db
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from faker import Faker
import random
import requests
import string


fake = Faker()

def fetch_random_image():
    try:
        response = requests.get('https://source.unsplash.com/featured/?profile_pic')
        response.raise_for_status()  
        return response.url
    except requests.exceptions.RequestException as e:
        print('Error fetching random image:', e)
        return None
    

def create_user(email, password, role):
    profile_picture = fetch_random_image()
    user = User(email=email, password=password, role=role, profile_picture=profile_picture)
    db.session.add(user)
    db.session.commit()
    return user

def create_teacher(user_id, image_url=None):  
    teacher = Teacher(
        user_id=user_id,
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        school=fake.company(),
        location=fake.address(),
        grade_or_course=fake.job(),
        image_url=image_url
    )
    db.session.add(teacher)

def create_substitute(user_id, image_url=None):
    substitute = Substitute(
        user_id=user_id,
        name=fake.name(),
        qualifications=fake.text(),
        location=fake.city(),
        grade_or_course=fake.job(),  
        phone=fake.phone_number(),  
        email=fake.email(), 
        verification_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),  
        image_url=image_url
    )
    db.session.add(substitute)

def create_site_admin(user_id):
    site_admin = SiteAdmin(user_id=user_id, name=fake.name())
    db.session.add(site_admin)

def create_users_and_roles(num_users):
    roles = ['Teacher', 'Substitute', 'Site Admin']
    teacher_created = False
    substitute_created = False
    admin_created = False

    for _ in range(num_users):
        email = fake.email()
        password = generate_random_password()
        role = random.choice(roles)
        user = create_user(email, password, role)

        if role == 'Teacher' and not teacher_created:
            create_teacher(user.id)
            teacher_created = True

        if role == 'Substitute' and not substitute_created:
            create_substitute(user.id)
            substitute_created = True

        if role == 'Site Admin' and not admin_created:
            create_site_admin(user.id)
            admin_created = True

        if teacher_created and substitute_created and admin_created:
            break

    if not teacher_created:
        create_teacher(user.id)

    if not substitute_created:
        create_substitute(user.id)

    if not admin_created:
        create_site_admin(user.id)

def create_courses_and_reviews(num_courses, teachers, substitutes):
    for _ in range(num_courses):
        teacher = random.choice(teachers)
        substitute = random.choice(substitutes)

        course = Course(
            teacher_id=teacher.user_id,
            substitute_id=substitute.user_id,
            class_subject=fake.job(),
            date=fake.date_this_year(),
            time=fake.time(),
            status=random.choice(['Scheduled', 'Completed', 'Canceled'])
        )
        db.session.add(course)
        db.session.commit()

        review = Review(
            writer_id=random.choice([teacher.user_id, substitute.user_id]),
            course_id=course.id,
            rating=random.randint(1, 5),
            comment=fake.text()
        )
        db.session.add(review)

    db.session.commit()

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def seed_database(num_users=5, num_courses=10):
    with app.app_context():
        print("Wiping old Data...")
        db.drop_all()
        db.create_all()
        print("Complete")

        print("Generating Users and Roles...")
        create_users_and_roles(num_users)
        print("Complete")

      
        teachers = Teacher.query.all()
        substitutes = Substitute.query.all()

       
        if teachers and substitutes:
            print("Generating Courses and Reviews...")
            create_courses_and_reviews(num_courses, teachers, substitutes)
            print("Complete")
        else:
            print("No teachers or substitutes found in the database. Skipping course and review generation.")

        db.session.commit()

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")
