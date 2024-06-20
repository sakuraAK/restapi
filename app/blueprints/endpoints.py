from flask import Blueprint, request, json
# from ..models.course import Course
from ..extensions import db, Course
from sqlalchemy import select


endpoints_blueprint = Blueprint('api', __name__, url_prefix='/api')

list_of_courses = [
    {"id": 1, "name": "Course A"},
    {"id": 2, "name": "Course B"},
]
@endpoints_blueprint.route('/courses', methods=['GET','POST'])
def get_courses():
    if request.method == 'GET':
        stmt = select(Course)
        result = db.session.execute(stmt).scalars().all()
        result_list = []
        for r in result:
            result_list.append(r.to_dict())

        return result_list, 200
    else:
        new_course = Course()
        new_course.name = request.json["name"]
        new_course.description = request.json["description"]
        session = db.session
        session.add(new_course)
        session.commit()
        return new_course.to_dict(), 200


