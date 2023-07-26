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
    db.session.commit()

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
    db.session.commit()

def create_site_admin(user_id):
    site_admin = SiteAdmin(user_id=user_id, name=fake.name())
    db.session.add(site_admin)
    db.session.commit()

def create_users_and_roles(num_teachers=10, num_subs=5, num_admins=2):
    for _ in range(num_teachers):
        email = fake.email()
        password = generate_random_password()
        user = create_user(email, password, 'Teacher')
        create_teacher(user.id)

    for _ in range(num_subs):
        email = fake.email()
        password = generate_random_password()
        user = create_user(email, password, 'Substitute')
        create_substitute(user.id)

    for _ in range(num_admins):
        email = fake.email()
        password = generate_random_password()
        user = create_user(email, password, 'Site Admin')
        create_site_admin(user.id)

    db.session.commit()

def create_courses_and_reviews(num_courses=10, num_reviews=5):
    teachers = Teacher.query.all()
    substitutes = Substitute.query.all()

    if not teachers or not substitutes:
        print("No teachers or substitutes found in the database. Skipping course and review generation.")
        return

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

    courses = Course.query.all()

    for _ in range(num_reviews):
        course = random.choice(courses)
        writer = random.choice([course.teacher, course.substitute])
        
        review = Review(
            writer_id=writer.id,
            course_id=course.id,
            rating=random.randint(1, 5),
            comment=fake.text()
        )
        db.session.add(review)

    db.session.commit()


def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def seed_database(num_teachers=10, num_subs=5, num_admins=2, num_courses=10, num_reviews=5):
    with app.app_context():
        print("Wiping old Data...")
        db.drop_all()
        db.create_all()
        print("Complete")

        print("Generating Users and Roles...")
        create_users_and_roles(num_teachers, num_subs, num_admins)
        print("Complete")

        print("Generating Courses and Reviews...")
        create_courses_and_reviews(num_courses, num_reviews)
        print("Complete")

        db.session.commit()

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")