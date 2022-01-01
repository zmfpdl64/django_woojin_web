from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Category, Tag #지금 있는 폴더에 models.py에서 Post 함수를 가져온다.
from django.core.exceptions import PermissionDenied #post, get 방식을 사용할 떄 권한이 있는가를 판단한다.

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
    def get_context_data(self, **kwargs):
       context = super(PostDetail, self).get_context_data()
       context['categories'] = Category.objects.all()
       context['no_category_post_count'] = Post.objects.filter(category=None).count()
       return context

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

def category_page(request, slug):

    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    #category = Category.objects.get(slug=slug)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tag' : tag,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
        }
    )

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView): #Mixin은 로그인을 정상적으로 했을 때만 보인다.
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
