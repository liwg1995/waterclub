from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('classes/', views.ClassListView.as_view(), name='classes'),
    path('enrollment/', views.enrollment, name='enrollment'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('gallery/', views.GalleryListView.as_view(), name='gallery'),
    path('contact/', views.contact, name='contact'),
]
