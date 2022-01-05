from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comment, Post, Category, Tag #지금 있는 폴더에 models.py에서 Post 함수를 가져온다.
from django.core.exceptions import PermissionDenied #post, get 방식을 사용할 떄 권한이 있는가를 판단한다.
from django.utils.text import slugify
from .forms import CommentForm
from django.db.models import Q


class PostList(ListView):
    model = Post
    ordering = '-pk' #CBV로 만든 함수이다. ordering은 제작된 순서로 포스트를 나타낸다.
    #template_name = 'blog/index.html' #템플릿 네임을 post_list.html에서 index.html로 변경한다.
     #매소드들이 있는데 그 중에 post_list 변수로 html에서 조작해야 한다.
    paginate_by = 5

    def get_context_data(self, **kwargs): #이렇게 정의되어있는 함수는 무조건 실행이 된다.
        context = super(PostList, self).get_context_data() #기존의 post_list = self.objects.all() 이라는 함수를 오바라이딩해서 값을 가져온다.
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post
   # template_name = "blog/single_post_page.html"
    def get_context_data(self, **kwargs):
       context = super(PostDetail, self).get_context_data()
       context['categories'] = Category.objects.all()
       context['no_category_post_count'] = Post.objects.filter(category=None).count() #필터안 조건이 참인 레코드 갯수
       context['comment_form'] = CommentForm
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
    post_list = tag.post_set.all() #post_set으로 tag에 특정 슬러그와 ForeignKey로 연결되어 있는 Post 레코드를 불러올 수 있다.
    #이때 모델명을 소문자로 쓰고 뒤에 _set을 붙이는 게 기본 설정이다.

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
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category'] #화면에 출력되는 필드들 
    #html에서 사용하는 변수 이름은 form이다. CreateView에서 내제되어있는 함수 또는 변수

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):#방문자가 폼에 담아 보낸 유효한 정보를 사용해 포스트를 만들고, 이 포스트의 고유 경로로 보내주는 redirect 역할을 한다.
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip() #전달받은 문자열의 왼쪽과 오른쪽에서 제거한다. 인자가 아무것도 없으면 공백을 제거한다.

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';') #;구분자를 기준으로 리스트를 생성한다.

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
           # return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):   #기존에 있는 태그들 불러와서 하나의 리스트를 만들어 context에 저장한다.
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list) #리스트를 문자열로 변환
        return context #기존 tags를 post_update_form.html로 'tags_str_default'라는 key에 넣어서 전달한다.

    def dispatch(self, request, *args, **kwargs):   #지금 로그인 사용자와 작성자와 비교해서 맞으면 실행한다. 또한 글을 쓸 수 있는 권한인지 확인한다.
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str') #post_update_form에서 보낸 form형식의 name이 tags_str인 input값을 가져온다. 문자열이다.
        if tags_str:#문자열이 존재한다면 실행
            tags_str = tags_str.strip() #공백 제거
            tags_str = tags_str.replace(',', ';') #구분자 ;로 통일
            tags_list = list()
            tags_list = tags_str.split(';') #;를 기준으로 리스트 형식으로 저장

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)#기존 Tag Db에서 name이 t인 레코드 가져온다 존재하면 tag에 레코드 주입
                #없으면 is_tag_created에는 false가 들어간다.
                if is_tag_created: #is_tag_created가 참이면
                    tag.slug = slugify(t, allow_unicode=True) #tag.slug에 slugify를 통해 slug형식으로 변환해 tag.slug에 저장한다.
                    tag.save()  #이후 db를 저장한다.
                self.object.tags.add(tag)

        return response

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class PostSearch(PostList):
    paginate_by = None
    
    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] =  f'Search: {q} ({self.get_queryset().count()})'

        return context