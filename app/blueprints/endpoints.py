from flask import Blueprint, request, json
from sqlalchemy import select
from database import Course, session, User, Program, Semester


endpoints_blueprint = Blueprint('api', __name__, url_prefix='/api')

@endpoints_blueprint.route('/courses', methods=['GET','POST'])
def courses():
    if request.method == 'GET':
        stmt = select(Course)
        result = session.execute(stmt).scalars().all()
        result_list = []
        for r in result:
            result_list.append(r.to_dict())

        return result_list, 200
    else:
        new_course = Course()
        new_course.name = request.json["name"]
        new_course.description = request.json["description"]
        new_course.total_hours = request.json["total_hours"]
        session.add(new_course)
        session.commit()
        return new_course.to_dict(), 200
@endpoints_blueprint.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'GET':
        stmt = select(User)
        result = session.execute(stmt).scalars().all()
        result_list = []
        for r in result:
            result_list.append(r.to_dict())

        return result_list, 200
    else:
        new_user = User()
        new_user.name = request.json["name"]
        new_user.role = request.json["role"]
        new_user.program_id = request.json["program_id"]
        new_user.active = request.json["active"]
        session.add(new_user)
        session.commit()
        return new_user.to_dict(), 200

@endpoints_blueprint.route('/programs', methods=['GET','POST'])
def programs():
    if request.method == 'GET':
        stmt = select(Program)
        result = session.execute(stmt).scalars().all()
        result_list = []
        for r in result:
            result_list.append(r.to_dict())

        return result_list, 200
    else:
        new_program = Program()
        new_program.name = request.json["name"]
        new_program.description = request.json["description"]
        new_program.total_hours = request.json["total_hours"]
        session.add(new_program)
        session.commit()
        return new_program.to_dict(), 200

@endpoints_blueprint.route('/semesters', methods=['GET','POST'])
def semesters():
    if request.method == 'GET':
        stmt = select(Semester)
        result = session.execute(stmt).scalars().all()
        result_list = []
        for r in result:
            result_list.append(r.to_dict())

        return result_list, 200
    else:
        new_semester = Semester()
        new_semester.season = request.json["season"]
        new_semester.start_date = request.json["start_date"]
        new_semester.end_date = request.json["end_date"]
        session.add(new_semester)
        session.commit()
        return new_semester.to_dict(), 200

@endpoints_blueprint.route('semesters-courses/<int:course_id>/<int:semester_id>', methods=['POST'])
def assign_course(course_id, semester_id):
    try:
        course = session.get(Course, course_id)
        semester = session.get(Semester, semester_id)
        semester.courses.append(course)
        session.add(semester)
        session.commit()
        return "All is well", 200
    except:
        return "Ooops", 500

@endpoints_blueprint.route('semesters-courses-students/<int:semester_id>/<int:course_id>/<int:student_id>' \
                           ,methods=['POST'])
def register_student(student_id, semester_id, course_id):
    try:
        student = session.get(User, student_id)
        if student.role != 'STUDENT':
            raise Exception('Not a student')
        semester = session.get(Semester, semester_id)
        for course in semester.courses:
            if course.id == course_id:
                course.users.append(student)
                return 'Done', 200
        raise Exception('Course does not exist')
    except Exception as e:
        print(e)
        return "Something went wrong", 500