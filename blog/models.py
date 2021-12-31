from django.db import models
import os
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    hook_text = models.CharField(max_length=100, blank=True)

    head_image = models.ImageField(upload_to ='blog/images/%Y/%m/%d/', blank=True) #년 월 일로 폴더를 구분해서 접근 시간을 단축시킨다.
    #blank는 비어있어도 경고 없이 실행이 가능하다는 뜻이다.
    file_upload = models.FileField(upload_to ='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}' #해당 포스트의 pk 값 해당 포스트의 title 값

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)  #파일 경로를 찾아내는 함수

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  #확장자를 찾아주는 함수