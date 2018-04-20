from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from uvigo.models import Student, Group, Teacher, Classroom, Topology, Indications, TeacherSchedule, Schedule


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    name = serializers.CharField()
    password = serializers.CharField()
    office = serializers.CharField(required=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.CharField()


class UserByTypeSerializer(serializers.Serializer):
    students = UserSerializer(many=True)
    teachers = UserSerializer(many=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)


class GroupViewSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    type = serializers.IntegerField(required=False)
    subject = serializers.CharField(required=False)


class ModifyGroupSerializer(serializers.Serializer):
    code = serializers.CharField()
    subject_name = serializers.CharField()
    number = serializers.IntegerField()
    teacher = serializers.IntegerField(required=False)
    classroom = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        instance.subject_name = validated_data['subject_name']
        instance.number = validated_data['number']
        instance.teacher = validated_data['teacher']
        instance.classroom = validated_data['classroom']

    def create(self, validated_data):
        group = Group.create_new_group(
            code=validated_data['code'],
            subject_name=validated_data['subject_name'],
            number=validated_data['number'],
            teacher=validated_data['teacher'],
            classroom=validated_data['classroom']
        )
        group.save()


class FCMSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)


class TeacherScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherSchedule
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'email', 'office', 'schedules')

    def get_schedules(self, obj):
        """obj is a Teacher instance. Returns list of dicts"""
        schedules = TeacherSchedule.objects.filter(teacher__id=obj.id)
        return [TeacherScheduleSerializer(schedule).data for schedule in schedules]


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ('id', 'name',)

class ScheduleWithoutGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('id', 'day', 'start_hour', 'finish_hour')

class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classroom = ClassroomSerializer()
    schedule = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Group
        fields = ('code', 'number', 'subject_name', 'teacher', 'classroom', 'schedule')

    def get_schedule(self, obj):
        """obj is a Group instance. Returns list of dicts"""
        schedules = Schedule.objects.filter(group_id=obj.code)
        return [ScheduleWithoutGroupSerializer(schedule).data for schedule in schedules]


class ProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Student
        fields = ('id', 'name', 'email', 'groups')

    def get_groups(self, obj):
        """obj is a Student instance. Returns list of dicts"""
        groups = Group.objects.filter(students__id=obj.id)
        return [GroupSerializer(group).data for group in groups]


class TopologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Topology
        fields = '__all__'


class IndicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indications
        fields = '__all__'


class FullClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    group = GroupSerializer()

    class Meta:
        model = Schedule
        fields = ('id', 'day', 'start_hour', 'finish_hour', 'group')
