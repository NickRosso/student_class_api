from app.models import Course, Grade
from django.db.models import Avg

class EnrollmentService(object):
    def get_courses(self, student):
        """ get_courses returns a queryset of courses 
        a student is enrolled sorted by id.
        Input: 
            - student(object)
        Output:
            - <Queryset : Course>
        """
        queryset = student.courses.all().order_by('id')
        return queryset

    def get_students(self, course):
        """ get_students returns a queryset of students 
        enrolled in a course sorted by their id.
        Input: 
            - student(object)
        Output:
            - <Queryset : Student>
        """
        queryset = course.students.all().order_by('id')
        return queryset

    def enroll(self, student, course):
        """ enrolls a student into a course 
        as long as all 3 criteria are met
        We check 3 things:
            - if the course exists
            - if the couse has less than 20 students
            - if a student is not currently is enrolled in the course
        Input: 
            - student(object), course(object)
        Output:
            - None
        """
        if Course.objects.filter(name=course.name).exists():
            course_object = Course.objects.get(name=course.name)
            if course_object.students.count() < 20: #check if its less than 20 since after the object is saved it be full at 20.
                if student not in course_object.students.all():
                    course_object.students.add(student)
                    course_object.save()
                    student.courses.add(course)
                    student.save()
                else:
                    raise Exception("student is trying to enroll in a course they already are enrolled in. They must really like the course...")
            else:
                raise Exception("student is trying to enroll in course which is currently full")
        else:
            raise Exception("student is trying to enroll in course which does not exist")

    def disenroll(self, student, course):
        """ disenrolls a student from a course
        Input: 
            - student(object), course(object)
        Output:
            - None
        """
        if student in course.students.all():
            course.students.remove(student)
            student.courses.remove(course)
            course.save()
            student.save()

def convert_grade_to_letter(grade):
    """ This function converts a grade to its letter grade. It does not support +/- letter grade notation.
    Input: 
        - grade(integer)
    Output:
        - string
    """
    if grade < 60:
        return 'F'
    elif grade < 70:
        return 'D'
    elif grade < 80:
        return 'C'
    elif grade < 90:
        return 'B'
    elif grade < 100:
        return 'A'
class GradeService(object):

    def assign_grade(self, course, student, grade):
        """ assign_grade Creates a grade object tied to a student and a course.
        We check 2 things:
            - The grades value is in 0-100
            - There currently exists no grade for a student and a course. (we have another function for this)
        Input: 
            - student, course, grade
        Output:
            - None
        """
        if student in course.students.all() and grade in range(0,101):
            if not Grade.objects.filter(course=course, student=student).exists():
                grade_object = Grade(course=course, student=student, value=grade)
                grade_object.save()
            else:
                raise Exception("student already has grade. Use adjust_grade instead.")
        else:
            raise Exception("student name is not enrolled in course")

    def adjust_grade(self, course, student, grade):
        """ adjust_grade Updates a grade object with a new value as long as the grade object exists and the value is 0-100.
        Input: 
            - course, student, grade
        Output:
            - None
        """
        if Grade.objects.filter(student=student, course=course).exists() and grade in range(0,101):
            grade_object = Grade.objects.get(student=student, course=course)
            grade_object.value = grade
            grade_object.save()
        else:
            raise Exception("Grade cannot be adjusted. None found for student in course")

    def get_grade(self, course, student):
        """ get_grade returns a grade object for a student in a given course. We raise a exception if their is no
        grade for a student in a course.
        Input: 
            - course, student
        Output:
            - grade.value
        """
        if Grade.objects.filter(student=student, course=course).exists():
            grade_object = Grade.objects.get(student=student, course=course)
            return grade_object.value
        else:
            raise Exception("Grade not found for student in course")

    def get_average_grade(self, course=None, student=None, is_letter_grade=False):
        """ 
        get_average_grade returns a integer value of the average grade. This function returns
        the average letter grade, or the average grade integer depending on the is_letter_grade.
            - If Course and Student is defined this function returns the students average grade in the course.
            - if a Course is defined and a student is not, we return the Course's average grade. 
        Input: 
            - course(object), student(object), is_letter_grade(bool)
        Output:
            - average_grade(integer) or letter grade(string)
        """
        if course == None:
            raise Exception("course name must be specified")

        elif course != None and student == None:
            average_grade = Grade.objects.filter(course=course).aggregate(Avg('value'))
            average_grade = round(average_grade['value__avg'])
            if is_letter_grade == True:
                return convert_grade_to_letter(average_grade) #helper function to convert to letter grade
            else:
                return average_grade

        elif student != None and course != None: 
            if student in course.students.all():
                average_grade = Grade.objects.filter(student=student, course=course).aggregate(Avg('value'))
                average_grade = round(average_grade['value__avg']) #round to the nearest whole number
                if is_letter_grade == True:
                    return convert_grade_to_letter(average_grade) #helper function to convert to letter grade
                else:
                    return average_grade
            else:
                raise Exception("student is not enrolled in course")