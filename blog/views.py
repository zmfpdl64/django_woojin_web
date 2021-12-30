from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')      #Post.objects.all()은 views.py에서 데이터베이스에 쿼리를 날려 원하는 레코드를 가져올 수 있다.
                                    #쿼리문으로는 all()이외에도 filter(), order_by(), create(), delete()등으로 다양하다.
    return render(                  #여기서 render를 통해 실행되는데 blog/index.html이 실행되고 여기에 전달되는 값은 request와 post값이다.
        request,
        'blog/index.html',
        {
            'posts': posts,   #key값은 내가 html에서 사용할 변수이름이고 posts는 값을 불러들인값을 value로 저장할 변수이다.
        }                       #key: value형식이 아닌 하나의 변수만 보내니 오류가 발생한다.
    )