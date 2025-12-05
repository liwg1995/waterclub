from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from apps.cms.models import Banner, Article, Gallery
from apps.classes.models import ClassType, Course, Enrollment
from apps.teachers.models import Teacher
from apps.students.models import Student


def home(request):
    """首页"""
    banners = Banner.objects.filter(is_active=True)[:5]
    featured_articles = Article.objects.filter(is_published=True, is_featured=True)[:3]
    class_types = ClassType.objects.filter(is_active=True)[:6]
    
    context = {
        'banners': banners,
        'featured_articles': featured_articles,
        'class_types': class_types,
    }
    return render(request, 'cms/home.html', context)


def about(request):
    """关于我们"""
    return render(request, 'cms/about.html')


class TeacherListView(ListView):
    """师资介绍"""
    model = Teacher
    template_name = 'cms/teachers.html'
    context_object_name = 'teachers'
    queryset = Teacher.objects.filter(status='active')


class ClassListView(ListView):
    """班型展示"""
    model = ClassType
    template_name = 'cms/classes.html'
    context_object_name = 'class_types'
    queryset = ClassType.objects.filter(is_active=True)


class ArticleListView(ListView):
    """文章列表"""
    model = Article
    template_name = 'cms/articles.html'
    context_object_name = 'articles'
    queryset = Article.objects.filter(is_published=True)
    paginate_by = 10


class ArticleDetailView(DetailView):
    """文章详情"""
    model = Article
    template_name = 'cms/article_detail.html'
    context_object_name = 'article'
    
    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj


class GalleryListView(ListView):
    """作品展示"""
    model = Gallery
    template_name = 'cms/gallery.html'
    context_object_name = 'gallery_items'
    queryset = Gallery.objects.filter(is_active=True)


def enrollment(request, class_type_id=None):
    """报名课程"""
    if request.method == 'POST':
        # 处理报名
        try:
            # 获取或创建学生
            student, _ = Student.objects.get_or_create(
                phone=request.POST.get('phone'),
                defaults={
                    'real_name': request.POST.get('name'),
                    'email': request.POST.get('email'),
                }
            )
            
            # 获取课程
            course_id = request.POST.get('course_id')
            course = get_object_or_404(Course, pk=course_id)
            
            # 检查是否已经报名
            enrollment_obj, created = Enrollment.objects.get_or_create(
                student=student,
                course=course,
                defaults={
                    'status': 'pending',
                    'source': '线上',
                }
            )
            
            if created:
                # 新报名，跳转到支付页面
                return redirect(f'/api/payment/create/?enrollment_id={enrollment_obj.pk}')
            else:
                # 已经报名
                return render(request, 'cms/enrollment_result.html', {
                    'message': '你已经报名过该课程',
                    'enrollment': enrollment_obj
                })
        except Exception as e:
            return render(request, 'cms/enrollment_error.html', {
                'error': str(e)
            })
    
    # GET请求，显示报名表单
    courses = Course.objects.filter(is_open_enrollment=True, status='enrolling')
    
    context = {
        'courses': courses,
        'selected_class_type_id': class_type_id,
    }
    return render(request, 'cms/enrollment.html', context)


def contact(request):
    """联系我们"""
    if request.method == 'POST':
        from apps.cms.models import Contact
        Contact.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        return render(request, 'cms/contact_success.html')
    return render(request, 'cms/contact.html')
