from rest_framework import serializers
from apps.classes.models import DanceType, ClassType, Course, ClassRoom, ClassSchedule, Enrollment


class DanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanceType
        fields = '__all__'


class ClassTypeSerializer(serializers.ModelSerializer):
    dance_type_name = serializers.CharField(source='dance_type.name', read_only=True)
    
    class Meta:
        model = ClassType
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class_type_name = serializers.CharField(source='class_type.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.real_name', read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['enrolled_count']


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class ClassScheduleSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.real_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    
    class Meta:
        model = ClassSchedule
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
