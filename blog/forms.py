from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta: #Meata라고 기입해서 에러가 발생했다. Meta도 의미가 있나보다... 상속과 오버라이드 공부를 좀 더 해야할 것 같다....
        model = Comment
        fields = ('content',)