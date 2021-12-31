from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Post, Category #지금 있는 폴더에 models.py에서 Post 함수를 가져온다.

class PostList(ListView):
    model = Post
    ordering = '-pk' #CBV로 만든 함수이다. ordering은 제작된 순서로 포스트를 나타낸다.
    #template_name = 'blog/index.html' #템플릿 네임을 post_list.html에서 index.html로 변경한다.
     #매소드들이 있는데 그 중에 post_list 변수로 html에서 조작해야 한다.

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context                                      

class PostDetail(DetailView):
    model = Post
   # template_name = "blog/single_post_page.html"

def index(request):
    posts = Post.objects.all().order_by('-pk')      #-pk 최신순
                                    #Post.objects.all()은 views.py에서 데이터베이스에 쿼리를 날려 원하는 레코드를 가져올 수 있다.
                                    #쿼리문으로는 all()이외에도 filter(), order_by(), create(), delete()등으로 다양하다.
    return render(                  #여기서 render를 통해 실행되는데 blog/index.html이 실행되고 여기에 전달되는 값은 request와 post값이다.
        request,
        'blog/index.html',
        {
            'posts': posts,   #key값은 내가 html에서 사용할 변수이름이고 posts는 값을 불러들인값을 value로 저장할 변수이다.
        }                       #key: value형식이 아닌 하나의 변수만 보내니 오류가 발생한다.
    )
"""
def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)  # .get(pk=pk) 괄호 안에 조건이 만족하는 레코드를 가져온다.

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )
    """