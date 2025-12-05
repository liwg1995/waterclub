from rest_framework import viewsets
from apps.attendance.models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    """考勤视图集"""
    queryset = Attendance.objects.select_related('student', 'schedule').all()
    serializer_class = AttendanceSerializer
    filterset_fields = ['status', 'student', 'schedule']
