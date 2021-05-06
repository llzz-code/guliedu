from datetime import datetime

from django.db import models

# Create your models here.
from DjangoUeditor.models import UEditorField


class CityInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='城市名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '城市信息'


class OrgInfo(models.Model):
    image = models.ImageField(upload_to='org/', max_length=200, verbose_name='机构图片')
    name = models.CharField(max_length=20, verbose_name='机构名称')
    course_num = models.IntegerField(default=0, verbose_name='课程数')
    study_num = models.IntegerField(default=0, verbose_name='学习人数')
    address = models.CharField(max_length=200, verbose_name='机构地址')
    desc = models.TextField(verbose_name='机构简介')
    detail = UEditorField(verbose_name='机构详情',
                          width=700,
                          height=400,
                          toolbars='full',
                          imagePath='ueditor/images/',
                          filePath='ueditor/files/',
                          upload_settings={'imageMaxSizing': 1024000},
                          default='')
    love_num = models.IntegerField(default=0, verbose_name='收藏数')
    click_num = models.IntegerField(default=0, verbose_name='访问数')
    category = models.CharField(choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')),
                                verbose_name='机构类别', max_length=10)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    city_info = models.ForeignKey(CityInfo, verbose_name='所属城市',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '机构信息'


class TeacherInfo(models.Model):
    image = models.ImageField(upload_to='teacher/', max_length=200, verbose_name='讲师头像')
    name = models.CharField(max_length=20, verbose_name='讲师姓名')
    work_year = models.IntegerField(default=3, verbose_name='工作年限')
    work_position = models.CharField(max_length=50, verbose_name='工作职位')
    work_style = models.CharField(max_length=20, verbose_name='教学特点')
    work_company = models.ForeignKey(OrgInfo, verbose_name='所属机构',
                                     on_delete=models.CASCADE)
    age = models.IntegerField(default=28, verbose_name='讲师年龄')
    gender = models.CharField(choices=(('girl', '女'), ('boy', '男')), max_length=10, verbose_name='性别',
                              default='girl')
    love_num = models.IntegerField(default=0, verbose_name='收藏数')
    click_num = models.IntegerField(default=0, verbose_name='访问数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '讲师信息'

