from django.db import models
import os
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) #카테고리의 이름을 의미한다.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    #사람이 읽을 수 있는 텍스트로 고유 URL을
    #만들고 싶을 때 주로 사용한다. Category 모델도 Post 모델처럼 pk를 활용해 URL을 만들 수도 있다.

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField()
    hook_text = models.CharField(max_length=100, blank=True)
    

    head_image = models.ImageField(upload_to ='blog/images/%Y/%m/%d/', blank=True) #년 월 일로 폴더를 구분해서 접근 시간을 단축시킨다.
    #blank는 비어있어도 경고 없이 실행이 가능하다는 뜻이다. upload_to는 모델즈의 기본인자로 upload_to에 파일 경로를 지정하여 저장한다.
    #%Y, %m, %d 는 지금 현재의 년 월 달 로 경로를 지정하는 것이다. /blank=True는 채우지 않아도 에러메시지가 출력이 안된다.
    file_upload = models.FileField(upload_to ='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now=True) #auto_now는 현재 시간을 나타낸다.
    updated_at = models.DateTimeField(auto_now=True) 

    author = models.ForeignKey(User, on_delete=models.CASCADE)  #작성자 필드를 생성하고 특성으로는 삭제됐을 때 작성자가 작성한 데이터들이 삭제된다.

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)#SET_NULL은 작성자가 DB에서 삭제됐을 때 공백으로 둔다는 의미
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}' #해당 포스트의 pk 값 해당 포스트의 title 값 , 작성자도 출력

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)  #파일 경로를 찾아내는 함수

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  #확장자를 찾아주는 함수

    def get_content_markdown(self):
        return markdown(self.content)

    