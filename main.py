from fastapi import FastAPI, HTTPException
from typing import List
from course import CourseManager, Course
from user import UserManager
from fastapi.security import APIKeyHeader

coursemanager = CourseManager()
usermanager = UserManager()
usermanager.create_a_user("John", "pwd", "student")
usermanager.create_a_user("Alice", "pwd", "teacher")
usermanager.create_a_user("Jimmy", "pwd", "student")

app = FastAPI()

@app.get("/")
def welcome():
    return "Welcome to miniCanvas!"

@app.post("/courses/{coursecode}")
def create_a_course(coursecode: str, 
                    request_body: dict):

    ### an admin should create a course
    semester = request_body.get("semester")
    teacher_id_list = request_body.get("teacher_id_list")

    if not semester or not teacher_id_list:
        raise HTTPException(status_code=422, detail="Request body must contain 'semester' and 'teacher_id_list'")

    teacher_list = usermanager.find_users(teacher_id_list)
    course_id = coursemanager.create_a_course(coursecode, semester, teacher_list)
    
    return course_id

@app.put("/courses/{courseid}/students")
def import_students(courseid: int,
                    request_body: dict):

    student_id_list = request_body.get("student_id_list")

    if not student_id_list:
        raise HTTPException(status_code=422, detail = "Request body must contain 'student_id_list'")
    
    course = coursemanager.find_a_course(courseid)

    if not course:
        raise HTTPException(status_code=404, detail=f"Course not found")

    student_list = usermanager.find_users(student_id_list)
    course.import_students(student_list)

    return {"message" : "Student added"}
    