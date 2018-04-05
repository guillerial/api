from rest_framework import serializers

from uvigo.models import Student, Group, Teacher, Classroom, Topology, Indications


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('name', 'email', 'office')


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ('name',)


class GroupSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    classroom = ClassroomSerializer()

    class Meta:
        model = Group
        fields = ('number', 'subject_name', 'teacher', 'classroom')


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

class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = '__all__'
