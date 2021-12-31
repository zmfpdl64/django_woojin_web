from django.urls import path
from . import views

urlpatterns = [
   # path('<int:pk>/', views.single_post_page),  #blog/뒤에 정수형태의 값이 들어온다면 이 정수값을 single_post_page에 pk라는 변수로 담아 보낸다.
   # path('', views.index),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()), #끝에 꼭 /슬래쉬 붙혀주기
    path('category/<str:slug>/', views.category_page),
]