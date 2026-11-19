
from django.contrib import admin
from .models import Student, Lecturer, Course, Venue, TimeSlot, Exam

admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Course)
admin.site.register(Venue)
admin.site.register(TimeSlot)
admin.site.register(Exam)
