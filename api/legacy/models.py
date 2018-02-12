from django.contrib.auth.hashers import make_password
from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Student(User):

    class Meta:
        db_table = 'students'

    @classmethod
    def create_new_student(cls, name, email, password):
        hashed_password = make_password(password, salt='markn', hasher='md5')

        return cls(name=name, email=email, password=hashed_password)




class Teacher(User):
    office = models.CharField(max_length=5)

    class Meta:
        db_table = 'teachers'


class Subject(models.Model):
    name = models.CharField(blank=False, max_length=50)
    code = models.CharField(blank=False, max_length=30)
    year = models.IntegerField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subjects'


class TeachersSubjects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    coordinator = models.BooleanField(default=False)

    class Meta:
        db_table = 'teachers_subjects'


class Classroom(models.Model):
    name = models.CharField(blank=False, max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'classrooms'


class Group(models.Model):
    number = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'groups'


class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day = models.IntegerField(blank=False)
    start_hour = models.IntegerField(blank=False)
    finish_hour = models.IntegerField(blank=False)
    start_date = models.DateField()
    finish_date = models.DateField()

    class Meta:
        db_table = 'schedules'
