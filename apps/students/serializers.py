from rest_framework import serializers
from apps.students.models import Student
from apps.users.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['student_no', 'total_spent', 'created_at', 'updated_at']
