from app import app, db  
from models import User, Teacher, Substitute, SiteAdmin, Course, Review, Request
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
    name = fake.name()
    location = fake.city()
    phone = fake.phone_number()
    profile_picture = fetch_random_image()
    user = User(name=name, email=email, location=location, phone=phone, password=password, role=role, profile_picture=profile_picture)
    db.session.add(user)
    db.session.commit()
    return user

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def create_teacher(user):
    school_name = fake.company()  
    teacher = Teacher(
        user_id=user.id,
        name=user.name,
        email=user.email,
        location=user.location,
        phone=user.phone,
        course_name=fake.job(),
        school_name=school_name,  
    )
    db.session.add(teacher)

def create_substitute(user):
    substitute = Substitute(
        user_id=user.id,
        name=user.name,
        email=user.email,
        location=user.location,
        phone=user.phone,
        qualifications=fake.text(),  
        verification_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    )
    db.session.add(substitute)

def create_site_admin(user):
    site_admin = SiteAdmin(
        user_id=user.id,
        name=user.name,
        email=user.email,
        phone=user.phone
    )
    db.session.add(site_admin)

def create_users_and_roles(num_teachers=10, num_subs=5, num_admins=2):
    for _ in range(num_teachers):
        email = fake.email()
        password = generate_random_password()
        user = create_user(email, password, 'Teacher')
        create_teacher(user)

    for _ in range(num_subs):
        email = fake.email()
        password = generate_random_password()
        user = create_user(email, password, 'Substitute')
        create_substitute(user)

    for _ in range(num_admins):
        email = fake.email()
        password = generate_random_password()
        user = create_user(email, password, 'SiteAdmin')
        create_site_admin(user)

def create_courses_and_reviews(num_courses=10, num_reviews=30):
    teachers = Teacher.query.all()
    substitutes = Substitute.query.all()

    if not teachers or not substitutes:
        print("No teachers or substitutes found in the database. Skipping course and review generation.")
        return

    course_review_pairs = set()

    for _ in range(num_courses):
        teacher = random.choice(teachers)
        substitute = random.choice(substitutes)

        while (teacher, substitute) in course_review_pairs:
            teacher = random.choice(teachers)
            substitute = random.choice(substitutes)

        course_review_pairs.add((teacher, substitute))

        school_name = fake.company()  
        school_location = fake.address()  

        course = Course(
            Correlating_teacher_ID=teacher.user_id,
            Correlating_substitute_ID=substitute.user_id,
            Course_name=fake.job(),
            Course_status=random.choice(['Available', 'Unavailable']),
            Course_school_name=school_name,  
            Course_location=school_location,  
        )
        db.session.add(course)

    db.session.commit()

    courses = Course.query.all()

    for _ in range(num_reviews):
        course = random.choice(courses)

        review = Review(
            Teacher_Id=course.Correlating_teacher_ID,
            Rating=random.randint(1, 5),
            Review=fake.text(),
            Correlating_Substitute_ID=course.Correlating_substitute_ID,
        )
        db.session.add(review)

    db.session.commit()

def create_single_request(substitute_id):
    teachers = Teacher.query.all()

    if not teachers:
        print("No teachers found in the database. Skipping request generation.")
        return

    teacher = random.choice(teachers)
    school_name = getattr(teacher, 'teacher_school', 'Unknown School')  
    school_location = getattr(teacher, 'school_location', 'Unknown Location')  

    request = Request(
        Substitute_user_id=substitute_id,
        Teacher_id=teacher.id,
        school_name=school_name,
        Teacher_school_location=school_location,
        Course_Being_covered=fake.job(),
        Confirmation=random.choice(['Accept', 'Decline']),
        Message_sub_sent_to=fake.email(),
        Teacher_if_declined=fake.text(),
    )
    db.session.add(request)
    db.session.commit()


def create_requests(num_requests=10):
    substitutes = Substitute.query.all()

    if not substitutes:
        print("No substitutes found in the database. Skipping request generation.")
        return

    num_requests = min(num_requests, len(substitutes))

    for _ in range(num_requests):
        substitute = random.choice(substitutes)
        create_single_request(substitute.user_id)

def seed_database(num_teachers=10, num_subs=5, num_admins=2, num_courses=10, num_reviews=30, num_requests=20):
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

        print("Generating SiteAdmin...")
        email = 'colly@example.com'
        password = 'Disney4Life!'
        user = create_user(email, password, 'SiteAdmin')
        create_site_admin(user)
        print("Complete")

        print("Generating Requests...")
        create_requests(num_requests)
        print("Complete")

if __name__ == '__main__':
    seed_database(num_teachers=10, num_subs=5, num_admins=2, num_courses=10, num_reviews=30, num_requests=10)
    print("Database seeded successfully!")