from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DanceTypeViewSet, ClassTypeViewSet, CourseViewSet,
                   ClassRoomViewSet, ClassScheduleViewSet, EnrollmentViewSet)

router = DefaultRouter()
router.register(r'dance-types', DanceTypeViewSet, basename='dancetype')
router.register(r'class-types', ClassTypeViewSet, basename='classtype')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'classrooms', ClassRoomViewSet, basename='classroom')
router.register(r'schedules', ClassScheduleViewSet, basename='schedule')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]
