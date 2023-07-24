from flask import Flask
from config import app, db
from models import User, Teacher, Substitute, SiteAdmin, Course, Review
from faker import Faker
from random import randint, choice as rc

app.app_context().push()

fake = Faker()

def create_user(email, password, role):
    user = User(email=email, password=password, role=role)
    db.session.add(user)
    db.session.commit()
    return user

def create_teacher(user_id):
    teacher = Teacher(user_id=user_id, name=fake.name(), contact_details=fake.address())
    db.session.add(teacher)

def create_substitute(user_id):
    substitute = Substitute(user_id=user_id, name=fake.name(), qualifications=fake.text())
    db.session.add(substitute)

def create_site_admin(user_id):
    site_admin = SiteAdmin(user_id=user_id, name=fake.name())
    db.session.add(site_admin)

def create_users_and_roles(num_users):
    roles = ['Teacher', 'Substitute', 'Site Admin']
    for _ in range(num_users):
        email = fake.email()
        user = create_user(email, 'password123', rc(roles))
        role = user.role
        if role == 'Teacher':
            create_teacher(user.id)
        elif role == 'Substitute':
            create_substitute(user.id)
        else:
            create_site_admin(user.id)

def create_courses_and_reviews(num_courses, teachers, substitutes):
    for _ in range(num_courses):
        teacher = rc(teachers)
        substitute = rc(substitutes)
        course = Course(
            teacher_id=teacher.id,
            substitute_id=substitute.id,
            class_subject=fake.job(),
            date=fake.date_this_year(),
            time=fake.time(),
            status=rc(['Scheduled', 'Completed', 'Canceled'])
        )
        db.session.add(course)
        review = Review(
            teacher_id=teacher.id,
            substitute_id=substitute.id,
            rating=randint(1, 5),
            comment=fake.text()
        )
        db.session.add(review)

def seed_database():
    print("Wiping old Data...")
    db.drop_all()
    db.create_all()
    print("Complete")

    num_users = 5
    num_courses = 10

    print("Generating Users and Roles...")
    create_users_and_roles(num_users)
    print("Complete")

    teachers = Teacher.query.all()
    substitutes = Substitute.query.all()

    print("Generating Courses and Reviews...")
    create_courses_and_reviews(num_courses, teachers, substitutes)
    print("Complete")

    db.session.commit()

if __name__ == '__main__':
    seed_database()
    print("Database seeded successfully!")
