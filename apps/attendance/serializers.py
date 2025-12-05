from rest_framework import serializers
from apps.attendance.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.real_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
