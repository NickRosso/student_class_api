from django.db import models

class Course(models.Model):
    """ Course Model contains a name and a m2m relationship to all the students in a course.
    Fields:
        course, student, value
    """
    name = models.CharField(max_length = 200, blank=False)
    students = models.ManyToManyField('Student')

    def save(self):
        if self.id == None:
            super(Course, self).save()
        elif self.students.count() <= 20 or self.students.count():
            super(Course, self).save()
        else:
            raise Exception(f'{self.name} already has 20 students. Course is full consider creating a another Course.')
class Grade(models.Model):
    """ Grade Model contains a single Course, and student that the grade is tied to. Something to explore would be the unique_together field
    to enforce at the model level, but in the service we prevent it in this implementation.
    We also have a value for the grade.
    Fields:
        course, student, value
    """
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING, blank=False)
    student = models.ForeignKey('Student', on_delete=models.DO_NOTHING, blank=False)
    value = models.IntegerField(default=0)

    def save(self):
        """ Overriding the Grade.save method to validate the value of a grade is in a range of 0-100 before saving. 
        This is already done in the services. But this will prevent an admin using a shell from defining it out of these ranges.
        """
        if self.value in range(0,101):
            super(Grade, self).save()
        else:
            raise Exception('Grade must be 0-101')

class Student(models.Model):
    """ Student Model contains a name of the student.
    We have a courses m2m relationship to determine the courses a student is enrolled in by just checking
    the student object.
    We probably could assign a m2m relationship for grades for a Student, but for the test cases, and usage of this didn't see the point.
    Fields:
        Name, and Courses.
    """
    name = models.CharField(max_length = 200, blank=False)
    courses = models.ManyToManyField('Course')
