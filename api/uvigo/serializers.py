from rest_framework import serializers

from uvigo.models import Student, Group, Teacher, Classroom, Topology, Indications, TeacherSchedule, Schedule


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TeacherScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherSchedule
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Teacher
        fields = ('name', 'email', 'office', 'schedules')

    def get_schedules(self, obj):
        """obj is a Teacher instance. Returns list of dicts"""
        schedules = TeacherSchedule.objects.filter(teacher__id=obj.id)
        return [TeacherScheduleSerializer(schedule).data for schedule in schedules]


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ('name',)


class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classroom = ClassroomSerializer()

    class Meta:
        model = Group
        fields = ('code', 'number', 'subject_name', 'teacher', 'classroom')


class ProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Student
        fields = ('name', 'email', 'groups')

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
        fields = ('day', 'start_hour', 'finish_hour', 'group')
