from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.students.models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """学员视图集"""
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['student_no', 'real_name', 'user__phone']
    filterset_fields = ['status']
