from audioop import reverse
from statistics import mode
from tkinter import CASCADE
from turtle import title
from django.db import models

# モデルをどのように保存するか
# Create your models here.
class Post(models.Model):
    # モデルではfieldをセット
    title = models.CharField(max_length= 50)
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # (https://4to.pics/article/post/13)
    def get_absolute_url(self):
        return reverse('list', kwargs={'pk': self.id})

#コメント機能に関するモデル
class Comment(models.Model):
    # コメント対象の指定
    subject = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='コメント')
    text = models.TextField('コメント')

    # datetime.datetime インスタンスによって表される日付と時刻です。(https://qiita.com/nachashin/items/f768f0d437e0042dd4b3)
    created_at = models.DateTimeField(auto_now_add=True,primary_key=True)
    # (https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q14243619389)

    # (https://www.nblog09.com/w/2019/05/14/django-field/)
    # id = models.BigAutoField(primary_key=True)

"""
class SubComment(models.Model):
    text = models.CharField('コメント', max_length=300)
    # コメントとサブコメントが1:M
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='紐付くコメント')
"""


