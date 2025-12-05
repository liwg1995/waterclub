from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.classes.models import DanceType, ClassType, Course, ClassRoom, ClassSchedule, Enrollment
from .serializers import (DanceTypeSerializer, ClassTypeSerializer, CourseSerializer,
                         ClassRoomSerializer, ClassScheduleSerializer, EnrollmentSerializer)


class DanceTypeViewSet(viewsets.ModelViewSet):
    """舞种视图集"""
    queryset = DanceType.objects.filter(is_active=True)
    serializer_class = DanceTypeSerializer


class ClassTypeViewSet(viewsets.ModelViewSet):
    """班型视图集"""
    queryset = ClassType.objects.filter(is_active=True).select_related('dance_type')
    serializer_class = ClassTypeSerializer
    filterset_fields = ['dance_type', 'level']


class CourseViewSet(viewsets.ModelViewSet):
    """课程视图集"""
    queryset = Course.objects.select_related('class_type', 'teacher').all()
    serializer_class = CourseSerializer
    filterset_fields = ['status', 'class_type', 'teacher']
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """学员报名"""
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        if course.is_full:
            return Response({'error': '该课程已满员'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not course.is_open_enrollment:
            return Response({'error': '该课程暂未开放报名'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建报名记录
        from apps.students.models import Student
        try:
            student = Student.objects.get(id=student_id)
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
                source=request.data.get('source', '线上')
            )
            course.enrolled_count += 1
            course.save()
            return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)
        except Student.DoesNotExist:
            return Response({'error': '学员不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClassRoomViewSet(viewsets.ModelViewSet):
    """教室视图集"""
    queryset = ClassRoom.objects.filter(is_active=True)
    serializer_class = ClassRoomSerializer


class ClassScheduleViewSet(viewsets.ModelViewSet):
    """排课视图集"""
    queryset = ClassSchedule.objects.select_related('course', 'teacher', 'classroom').all()
    serializer_class = ClassScheduleSerializer
    filterset_fields = ['course', 'status', 'teacher']


class EnrollmentViewSet(viewsets.ModelViewSet):
    """报名视图集"""
    queryset = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer
    filterset_fields = ['status', 'student', 'course']
