from dataclasses import fields
from django import forms
from .models import Post, Comment

# (https://noauto-nolife.com/post/django-m2m-form/)
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        # subject等の非表示
        fields = ('text',)
        labels = {'text':'コメント','subject':'投稿先'}
    """
        # 参考=(1-20 コメント投稿機能を付与する)
        def __init__(self,*args, **kwargs):
            kwargs.setdefault('label_suffix', '')
            super().__init__(*args, **kwargs)
            self.fields['user_name'].widget.attrs['value'] = '名無し'

        def save_with_topic(self, topic_id, commit=True):
            comment = self.save(commit=False)
            comment.topic = Post.objects.get(id=topic_id)
            comment.no = Comment.objects.filter(topic_id=topic_id).count() + 1
            if commit:
                comment.save()
            return comment
    """