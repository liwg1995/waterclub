from rest_framework import serializers
from apps.teachers.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        read_only_fields = ['teacher_no', 'created_at', 'updated_at']
