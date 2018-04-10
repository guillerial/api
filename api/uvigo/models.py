from django.contrib.auth.hashers import make_password, check_password
from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True, default=None, blank=True, null=True)
    password = models.CharField(max_length=100, default=None, blank=True, null=True)

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

    def check_password(self, plain_password):
        return check_password(plain_password, self.password)


class Teacher(User):
    office = models.CharField(max_length=5)

    class Meta:
        db_table = 'teachers'


class Classroom(models.Model):
    name = models.CharField(blank=False, max_length=5)
    nearby_beacon = models.CharField(max_length=20, null=True)
    last_indication = models.CharField(max_length=255, null=True)
    last_image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'classrooms'


class Group(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    subject_name = models.CharField(max_length=20)
    number = models.IntegerField(default=None, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, default=None)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True, default=None)
    students = models.ManyToManyField(Student)

    def __str__(self):
        return self.number

    class Meta:
        db_table = 'groups'


class Schedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    day = models.IntegerField(blank=False)
    start_hour = models.IntegerField(blank=True)
    finish_hour = models.IntegerField(blank=True)
    start_date = models.DateField(default=None, blank=True, null=True)
    finish_date = models.DateField(default=None, blank=True, null=True)

    class Meta:
        db_table = 'schedules'


class Topology(models.Model):
    route = models.CharField(primary_key=True, blank=False, max_length=50)
    next = models.CharField(blank=False, max_length=25)

    class Meta:
        db_table = 'topology'


class Indications(models.Model):
    route = models.CharField(primary_key=True, blank=False, max_length=50)
    indication = models.TextField(blank=False)
    image_url = models.CharField(blank=False, max_length=250)

    class Meta:
        db_table = 'indications'
