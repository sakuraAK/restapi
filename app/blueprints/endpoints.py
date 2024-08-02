from flask import Blueprint, request, json, Response
from sqlalchemy import select, or_
from database import Course, session, User, Program, Semester


endpoints_blueprint = Blueprint('api', __name__, url_prefix='/api')

@endpoints_blueprint.route('/courses', methods=['GET','POST'])
def courses():
    if request.method == 'GET':
        stmt = select(Course)
        filter = request.args.get("filter")
        if filter:
            stmt = select(Course).filter(Course.description.like(f"%{filter}%"))
            print(stmt)
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
@endpoints_blueprint.route('/users', methods=['GET','POST', 'PUT'])
def users():
    try:
        if request.method == 'GET':
            stmt = select(User)
            result = session.execute(stmt).scalars().all()
            result_list = []
            for r in result:
                result_list.append(r.to_dict())

            return result_list, 200
        elif request.method == 'POST':
            new_user = User()
            new_user.name = request.json["name"]
            new_user.role = request.json["role"]
            new_user.program_id = request.json["program_id"]
            new_user.active = request.json["active"]
            session.add(new_user)
            session.commit()
            return new_user.to_dict(), 200
        else:
            user = session.get(User, request.json["id"])
            if not user:
                return "User does not exist", 404
            user.name = request.json["name"]
            user.role = request.json["role"]
            user.program_id = request.json["program_id"]
            user.active = request.json["active"]
            session.commit()
            return user.to_dict(), 200
    except:
        return "Ooops", 500

@endpoints_blueprint.route('/users/<int:user_id>', methods=['DELETE', 'GET'])
def delete_user(user_id):
    user = session.get(User, user_id)
    if not user:
        return "User does not exist", 404
    if request.method == 'DELETE':
        session.delete(user)
        session.commit()
        return "User removed", 200
    else:
        return user.to_dict(), 200


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
        new_program.total_hours = request.json["totalHours"]
        session.add(new_program)
        session.commit()
        # resp = Response(new_program.to_dict(), 200)
        # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
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
                session.commit()
                return 'Done', 200
        raise Exception('Course does not exist')
    except Exception as e:
        print(e)
        return "Something went wrong", 500

@endpoints_blueprint.route('programs-courses/<int:program_id>/<int:course_id>', methods=['POST'])
def add_program_course(program_id ,course_id):
    program = session.get(Program, program_id)
    if not program:
        return "Program does not exist", 404
    course = session.get(Course, course_id)
    if not course:
        return "Course does not exist", 404
    for course in program.courses:
        if course.id == course_id:
            return "Course was added", 200
    program.courses.append(course)
    session.commit()
    return "Course was added", 200


@endpoints_blueprint.route('semesters-courses-teachers/<int:semester_id>/<int:course_id>/<int:teacher_id>' \
                           ,methods=['POST'])
def register_teacher(teacher_id, semester_id, course_id):
    try:
        teacher = session.get(User, teacher_id)
        if not teacher:
            return "User does not exist", 404

        if teacher.role != 'TEACHER':
            raise Exception('Wrong role')
        semester = session.get(Semester, semester_id)
        for course in semester.courses:
            if course.id == course_id:
                course.users.append(teacher)
                session.commit()
                return 'Done', 200
        return "Course does not exist", 404
    except Exception as e:
        print(e)
        return "Something went wrong", 500


@endpoints_blueprint.route('/programs/<int:id>', methods=['DELETE'])
def delete_program(id):
    program = session.get(Program, id)
    if not program:
        return "Program does not exist", 404
    session.delete(program)
    session.commit()
    return {"result": "Program removed"}, 200
