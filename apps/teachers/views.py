from rest_framework import viewsets
from apps.teachers.models import Teacher
from .serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    """教师视图集"""
    queryset = Teacher.objects.select_related('user').all()
    serializer_class = TeacherSerializer
    search_fields = ['real_name', 'specialty']
    filterset_fields = ['status', 'specialty']
