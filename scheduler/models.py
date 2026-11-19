
from django.db import models


class Student(models.Model):
    student_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name


class Lecturer(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.PROTECT
    )
    students = models.ManyToManyField(Student, related_name="courses")

    def __str__(self):
        return self.course_code


class Venue(models.Model):
    venue_name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.venue_name


class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start_time}"


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.course} - {self.time_slot}"
