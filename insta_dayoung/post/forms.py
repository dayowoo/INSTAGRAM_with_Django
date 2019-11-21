from django import forms
from .models import Post

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'content']
        widgets = {
        'content': forms.Textarea(attrs={'class': 'post-new-content',
        'rows': 5,
        'cols': 50, 
        'placeholder': '#태그명 을 통해서 검색 태그를 등록할 수 있습니다. \n 예시 :코딩연습 #멋쟁이사자처럼',})
        }
        labels = {
            'image': '',
            'content': ''
        }
        required = {
            'image':False,
        }