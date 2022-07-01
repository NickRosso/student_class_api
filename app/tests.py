from django.test import TestCase

from django.db.models import QuerySet

from app.models import Course, Student
from app.services import EnrollmentService, GradeService


class CourseCreationTestCase(TestCase):
    def test_create_course(self):
        course = Course(name='Math')
        course.save()
        self.assertEqual(course.name, 'Math')


class StudentCreationTestCase(TestCase):
    def test_create_student(self):
        student = Student(name='Alex')
        student.save()
        self.assertEqual(student.name, 'Alex')


class EnrollmentTestCase(TestCase):

    def test_enroll_student_in_course(self):
        student = Student(name='Alex')
        student.save()

        course = Course(name='Math')
        course.save()

        enrollment_service = EnrollmentService()

        self.assertIsInstance(enrollment_service.get_students(course), QuerySet)
        self.assertNotIn(student, list(enrollment_service.get_students(course)))

        self.assertIsInstance(enrollment_service.get_courses(student), QuerySet)
        self.assertNotIn(course, list(enrollment_service.get_courses(student)))

        enrollment_service.enroll(student, course)

        self.assertIn(student, list(enrollment_service.get_students(course)))
        self.assertIn(course, list(enrollment_service.get_courses(student)))

    def test_enroll_already_enrolled_student_in_course(self):
        student = Student(name='Alex')
        student.save()

        course = Course(name='Math')
        course.save()

        enrollment_service = EnrollmentService()

        enrollment_service.enroll(student, course)

        self.assertRaises(Exception, enrollment_service.enroll, student, course)

    def test_disenroll_student_from_course(self):
        student = Student(name='Alex')
        student.save()
        course = Course(name='Math')
        course.save()

        enrollment_service = EnrollmentService()

        enrollment_service.enroll(student, course)

        self.assertIn(student, list(enrollment_service.get_students(course)))
        self.assertIn(course, list(enrollment_service.get_courses(student)))

        enrollment_service.disenroll(student, course)

        self.assertNotIn(student, list(enrollment_service.get_students(course)))
        self.assertNotIn(course, list(enrollment_service.get_courses(student)))

    def test_disenroll_not_enrolled_student_from_course(self):
        student = Student(name='Alex')
        student.save()
        course = Course(name='Math')
        course.save()

        enrollment_service = EnrollmentService()

        self.assertNotIn(student, list(enrollment_service.get_students(course)))
        self.assertNotIn(course, list(enrollment_service.get_courses(student)))

        enrollment_service.disenroll(student, course)

        self.assertNotIn(student, list(enrollment_service.get_students(course)))
        self.assertNotIn(course, list(enrollment_service.get_courses(student)))

    def test_too_many_students_in_course(self):
        math = Course(name="Calculus")
        math.save()

        enrollment_service = EnrollmentService()

        for i in range(21):
            alex = Student(name=f"Alex{i}")
            alex.save()

            if i < 20:
                enrollment_service.enroll(alex, math)
            else:
                self.assertRaises(Exception, enrollment_service.enroll, alex, math)

    def test_with_many_courses_and_many_students(self):
        alex = Student(name="Alex")
        alex.save()
        jordan = Student(name="Jordan")
        jordan.save()

        math = Course(name="Math")
        math.save()
        biology = Course(name="Biology")
        biology.save()

        enrollment_service = EnrollmentService()

        enrollment_service.enroll(alex, math)
        enrollment_service.enroll(jordan, biology)
        enrollment_service.enroll(alex, biology)

        self.assertListEqual(list(enrollment_service.get_courses(alex)), [math, biology])
        self.assertListEqual(list(enrollment_service.get_courses(jordan)), [biology])

        self.assertListEqual(list(enrollment_service.get_students(biology)), [alex, jordan])

        self.assertListEqual(list(enrollment_service.get_students(math)), [alex])

        enrollment_service.disenroll(alex, biology)

        self.assertListEqual(list(enrollment_service.get_courses(alex)), [math])
        self.assertListEqual(list(enrollment_service.get_students(biology)), [jordan])

        enrollment_service.disenroll(jordan, math)
        self.assertListEqual(list(enrollment_service.get_courses(jordan)), [biology])
        self.assertListEqual(list(enrollment_service.get_students(math)), [alex])



class GradeTestCase(TestCase):

    def test_assign_grade_to_enrolled_student(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        grade_service.assign_grade(math, alex, 95)
        self.assertEqual(grade_service.get_grade(math, alex), 95)

    def test_assign_grade_to_unenrolled_student(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        grade_service = GradeService()
        self.assertRaises(Exception, grade_service.assign_grade, math, alex, 95)

    def test_assign_invalid_grade(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        self.assertRaises(Exception, grade_service.assign_grade, math, alex, 101)
        self.assertRaises(Exception, grade_service.assign_grade, math, alex, -5)

    def test_assign_existing_grade(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        grade_service.assign_grade(math, alex, 90)
        self.assertRaises(Exception, grade_service.assign_grade, math, alex, 92)

    def test_adjust_grade_for_enrolled_student(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        grade_service.assign_grade(math, alex, 90)
        grade_service.adjust_grade(math, alex, 91)
        self.assertEqual(grade_service.get_grade(math, alex), 91)

    def test_adjust_grade_for_unenrolled_student(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        grade_service = GradeService()
        self.assertRaises(Exception, grade_service.adjust_grade, math, alex, 91)

    def test_adjust_invalid_grade(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        grade_service.assign_grade(math, alex, 90)
        self.assertRaises(Exception, grade_service.adjust_grade, math, alex, 101)
        self.assertRaises(Exception, grade_service.adjust_grade, math, alex, -1)

    def test_adjust_missing_grade(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        self.assertRaises(Exception, grade_service.adjust_grade, math, alex, 90)

    def test_get_grade_for_graded_student(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)

        grade_service = GradeService()
        grade_service.assign_grade(math, alex, 90)
        self.assertEquals(grade_service.get_grade(math, alex), 90)

    def test_get_grade_for_missing_student(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        grade_service = GradeService()
        self.assertRaises(Exception, grade_service.get_grade, math, alex)

    def test_get_average_grade_for_nothing(self):
        grade_service = GradeService()
        self.assertRaises(Exception, grade_service.get_average_grade, course=None, student=None, is_letter_grade=True)
        self.assertRaises(Exception, grade_service.get_average_grade, course=None, student=None, is_letter_grade=False)

    def test_get_average_grade_for_empty_course(self):
        math = Course(name="math")
        math.save()

        grade_service = GradeService()

        self.assertRaises(Exception, grade_service.get_average_grade, course=math, is_letter_grade=True)
        self.assertRaises(Exception, grade_service.get_average_grade, course=math, is_letter_grade=False)

    def test_get_average_grade_for_student_and_course(self):
        alex = Student(name="Alex")
        alex.save()

        math = Course(name="Math")
        math.save()

        grade_service = GradeService()

        self.assertRaises(Exception, grade_service.get_average_grade, course=math, student=alex, is_letter_grade=True)
        self.assertRaises(Exception, grade_service.get_average_grade, course=math, student=alex, is_letter_grade=False)

    def test_get_average_grade_for_unenrolled_student(self):
        alex = Student(name="Alex")
        alex.save()

        grade_service = GradeService()

        self.assertRaises(Exception, grade_service.get_average_grade, student=alex, is_letter_grade=True)
        self.assertRaises(Exception, grade_service.get_average_grade, student=alex, is_letter_grade=False)

    def test_get_average_grade_for_enrolled_students(self):
        alex = Student(name="Alex")
        alex.save()

        jordan = Student(name="Jordan")
        jordan.save()

        math = Course(name="Math")
        math.save()

        enrollment_service = EnrollmentService()
        enrollment_service.enroll(alex, math)
        enrollment_service.enroll(jordan, math)

        grade_service = GradeService()

        grade_service.assign_grade(math, alex, 89)
        grade_service.assign_grade(math, jordan, 98)

        self.assertEqual(grade_service.get_average_grade(course=math, is_letter_grade=False), 94)
        self.assertEqual(grade_service.get_average_grade(course=math, is_letter_grade=True), "A")