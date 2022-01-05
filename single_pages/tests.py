from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from blog.models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')

        self.post_001 = Post.objects.create(
            title="첫 번째 포스트",
            content = "첫 번째 포스트입니다.",
            author = self.user_trump
        )

        self.post_002 = Post.objects.create(
            title="두 번째 포스트",
            content = "두 번째 포스트입니다.",
            author = self.user_obama
        )
        self.post_003 = Post.objects.create(
            title="세 번째 포스트",
            content = "세 번째 포스트입니다.",
            author = self.user_obama
        )
        self.post_004 = Post.objects.create(
            title="네 번째 포스트",
            content = "네 번째 포스트입니다.",
            author = self.user_obama
        )