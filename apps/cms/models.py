from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Banner(models.Model):
    """轮播图"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banners/')
    link = models.URLField('链接', null=True, blank=True)
    description = models.TextField('描述', null=True, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        db_table = 'banners'
        ordering = ['sort_order', '-created_at']
        app_label = 'cms'
    
    def __str__(self):
        return self.title


class Article(models.Model):
    """文章资讯"""
    
    CATEGORY_CHOICES = (
        ('news', '新闻动态'),
        ('activity', '活动公告'),
        ('performance', '演出作品'),
        ('tutorial', '教学心得'),
    )
    
    title = models.CharField('标题', max_length=200)
    category = models.CharField('分类', max_length=20, choices=CATEGORY_CHOICES)
    cover = models.ImageField('封面图', upload_to='articles/')
    summary = models.TextField('摘要', max_length=300)
    content = RichTextUploadingField('正文')
    author = models.CharField('作者', max_length=50, default='管理员')
    views = models.IntegerField('浏览量', default=0)
    is_published = models.BooleanField('是否发布', default=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    published_at = models.DateTimeField('发布时间', auto_now_add=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        db_table = 'articles'
        ordering = ['-published_at']
        app_label = 'cms'
    
    def __str__(self):
        return self.title


class Gallery(models.Model):
    """作品相册"""
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='gallery/')
    description = models.TextField('描述', null=True, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否显示', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '作品相册'
        verbose_name_plural = verbose_name
        db_table = 'gallery'
        ordering = ['sort_order', '-created_at']
        app_label = 'cms'
    
    def __str__(self):
        return self.title


class Contact(models.Model):
    """联系我们"""
    name = models.CharField('姓名', max_length=50)
    phone = models.CharField('联系电话', max_length=11)
    email = models.EmailField('邮箱', null=True, blank=True)
    subject = models.CharField('主题', max_length=100)
    message = models.TextField('留言内容')
    is_replied = models.BooleanField('是否回复', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '联系留言'
        verbose_name_plural = verbose_name
        db_table = 'contacts'
        ordering = ['-created_at']
        app_label = 'cms'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
