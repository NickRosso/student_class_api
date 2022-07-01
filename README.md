## Environment:
- Python version: 3.7
- Django version: 2.2.16

## Read-Only Files:
- app/tests.py
- manage.py

## Requirements:

In this challenge, your task is to build models and a service layer to represent courses, grades, and students.

The definitions and detailed requirements list follow. You will be graded on whether your application performs data retrieval and manipulation based on given use cases exactly as described in the requirements.

1. Each course must have the following fields:

id: a unique autoincrement integer ID of the course
name: a string denoting the name of the course


2. Each grade must have the following fields:

id: a unique autoincrement integer ID of the course
course: the related course the grade relates to
student: the related student the grade was given to
value: a positive integer from 0-100 (inclusive)


3. Each student must have the following fields:

id: a unique autoincrement integer ID of the student
name: a string denoting the name of the student


4. A course must be able to be created in the following way:

`math = Course(name='Math')`


5. A student must be able to be created in the following way:

`alex = Student(name='Alex')`


6. The `EnrollmentService` service implements the following methods...

    a. `get_students(course)` method, which returns a Queryset of all Students enrolled in the Course, sorted by their names in ascending order.

    b. `get_courses(student)` method, which returns a Queryset of all Courses the Student is enrolled in, sorted by their ids in ascending order.

    c. `enroll(student, course)` method, which enrolls the Student in the Course given as a parameter. If the student is already enrolled in the given course, an Exception is raised. No course can support more than 20 students and if students are attempted to enroll when a course is at capacity an Exception will be raised.

    d. `disenroll(student, course)` method, which disenrolls the Student from the Course given as a parameter. If the student is not enrolled in the given course, nothing happens.


7. Grades should be maintained via the `GradingService` service. This implements the following methods...

    a. `assign_grade(course, student, grade)` method, which saves the Grade given to a Student for taking a Course. If a Student is not enrolled in that Course an Exception is raised.

    b. `adjust_grade(course, student, grade)` method, which updates the Grade a Student received for taking a Course. If a Student is not enrolled in that Course an Exception is raised.

    c. `get_grade(self, course, student)` method, which gets the grade (as an integer) a Student received for taking a Course.

    d. `get_average_grade(course=None, student=None, is_letter_grade=False)` method, which returns the average Grade for a Course or Student, rounded to the nearest integer. Here are some further requirements:
        * Exactly one of a Course or Student can be provided as a parameter, otherwise an Exception is raised.
        * If an empty Course is provided, an Exception is raised.
        * If an unenrolled Student is provided, an Exception is raised.
        * If `is_letter_grade` is `True` then the average grade will be returned as a string letter grade (A-F). The letter mapping is as follows: F (0-59), D- (60-62), D (63-66), D+ (67-69), ..., A- (90-92), A (93-96), A+ (97-100).

Your task is to complete the given project so that it passes all the test cases when running the provided unit tests. The project by default supports the use of the SQLite3 database.

To view example usage see `app/tests.py`.


## Commands

+ run:
```source env1/bin/activate; pip3 install -r requirements.txt; python3 manage.py makemigrations && python3 manage.py migrate --run-syncdb && python3 manage.py runserver 0.0.0.0:8000```

+  install:
```bash python_install.sh;source env1/bin/activate; pip3 install -r requirements.txt;```

+ test:
```rm -rf unit.xml;source env1/bin/activate; python3 manage.py test```