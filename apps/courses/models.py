from datetime import datetime

from django.db import models

from DjangoUeditor.models import UEditorField
from orgs.models import TeacherInfo, OrgInfo


# Create your models here.


class CourseInfo(models.Model):
    image = models.ImageField(upload_to='course/', max_length=200, verbose_name='课程封面')
    name = models.CharField(max_length=20, verbose_name='课程名')
    study_time = models.IntegerField(default=0, verbose_name='学习时长')
    study_num = models.IntegerField(default=0, verbose_name='学习人数')
    level = models.CharField(choices=(('gj', '高级'), ('zj', '中级'), ('cj', '初级')),
                             verbose_name='课程难度', max_length=5, default='cj')
    love_num = models.IntegerField(default=0, verbose_name='收藏数')
    click_num = models.IntegerField(default=0, verbose_name='访问数')
    desc = models.TextField(verbose_name='课程简介')
    detail = UEditorField(verbose_name='课程详情',
                          width=700,
                          height=400,
                          toolbars='full',
                          imagePath='ueditor/images/',
                          filePath='ueditor/files/',
                          upload_settings={'imageMaxSizing': 1024000},
                          default='')
    category = models.CharField(choices=(('qd', '前端开发'), ('hd', '后端开发')),
                                verbose_name='课程类型', max_length=5)
    course_notice = models.CharField(max_length=50, verbose_name='课程公告',
                                     null=True, blank=True)
    course_need = models.CharField(max_length=100, verbose_name='课程须知',
                                   null=True, blank=True)
    teacher_tell = models.CharField(max_length=100, verbose_name='讲师提醒',
                                    null=True, blank=True)
    org_info = models.ForeignKey(OrgInfo, verbose_name='所属机构',
                                 on_delete=models.CASCADE)
    teacher_Info = models.ForeignKey(TeacherInfo, verbose_name='讲师',
                                     on_delete=models.CASCADE)
    is_banner = models.BooleanField(default=False,
                                    verbose_name='是否轮播')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '课程信息'


class LessonInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='章节名')
    course_info = models.ForeignKey(CourseInfo, verbose_name='所属课程',
                                    on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '章节信息'


class VideoInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='视频名称')
    study_time = models.IntegerField(default=0, verbose_name='视频时长')
    url = models.URLField(default='http://www.atguigu.com', verbose_name='视频链接', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    lesson_info = models.ForeignKey(LessonInfo, verbose_name='所属章节',
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '视频信息'


class SourceInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='资源名称')
    download = models.FileField(upload_to='source/', verbose_name='资源链接', max_length=200)
    course_info = models.ForeignKey(CourseInfo, verbose_name='所属课程',
                                    on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '资源信息'

