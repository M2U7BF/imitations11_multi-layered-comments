from audioop import reverse
from dataclasses import fields
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Post
from .models import Comment
# from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from random import randint
from django.http import request

"""
CreateViewとはデータの作成をする際に用いられる汎用view。
例えば、記事や写真を投稿したり、会員登録をしたりするページで使われます。

このような投稿機能や会員登録機能は多くのWebページで実装されているため、
クラスベースビューでのDjango開発ではCreateViewの使用頻度はとても高いです。
(https://kosuke-space.com/django-createview)

①アプリのurls.pyにURLを記述しておき、
②処理を記述し
③読み込みテンプレートをセットする。
"""
# 一覧画面
class ListClass(ListView) :
    template_name = 'list.html'
    model = Post


    # (https://qiita.com/yongjugithub/items/edd69e1ac6d4507f9ad1)
    queryset = Post.objects.order_by('-created_at')
    # (https://qiita.com/yongjugithub/items/edd69e1ac6d4507f9ad1)
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["comment_list"] = Comment.objects.all()
        return context

# Post投稿画面
class FormClass(CreateView):
    template_name = 'form.html'
    # DBに反映するためにモデルもセット
    model = Post
    fields = ('title','memo')
    # 投稿完了時の遷移先
    success_url = reverse_lazy('list')

# Post編集画面
# 参考(https://noumenon-th.net/programming/2019/11/19/django-updateview/)
class PostUpdate(UpdateView):
    template_name = 'edit_posts.html'
    model = Post
    fields = ('title','memo')

    # 修正(https://itc.tokyo/2021/08/29/5306/)
    # UpdateViewの処理の後の遷移先
    def get_success_url(self):
        return reverse_lazy('list')
    
    def get_form(self):
        form = super(PostUpdate, self).get_form()
        form.fields['title'].label = 'タイトル'
        form.fields['memo'].label = '本文'
        return form

# (https://noauto-nolife.com/post/django-m2m-form/)
class IndexView(View):
    def get(self, request, *args, **kwargs):
        form    = CommentForm()
        data    = Comment.objects.order_by("created_at")
        context = { "data":data,
                    "form":form}

        return render(request,"websites/list.html",context)

    def post(self, request, *args, **kwargs):
        form    = CommentForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("list")

    index   = ListClass.as_view()

"""
# Comment投稿画面
# (https://rurukblog.com/post/djangopkurlmv/)
def CommentView(request,pk):          # (1)requestを設定しないとエラーになる
    s = Post.objects.get(pk=pk)     # (2)Potsテーブルからpkで指定したレコードを取得
    url = s.url                       # (5)Postテーブルからpostのurlを取得
    comment_url = '/post/' + url + '/'    # (6)post_detail.htmlに遷移するためのurlを作成
    return redirect(comment_url)  
"""

# Comment投稿画面
class CommentForm(CreateView):
    template_name = 'comment_form.html'
    model = Comment
    fields = ['text','subject']

    # コメント投稿画面に投稿先を表示
    def get_context_data(self):
        ctxt = super().get_context_data()
        # テンプレートに渡すための変数名作成(https://chuna.tech/detail/46/#i3-2)
        ctxt["object_list"] = Post.objects.all()
        return ctxt

    def get_form(self):
        form = super(CommentForm, self).get_form()
        form.fields['subject'].label = '題'
        # フィールドの初期値の設定(https://k-mawa.hateblo.jp/entry/2017/10/31/235640)
        form.initial['subject'] = self.kwargs['pk']
        form.fields['text'].required = True
        return form
    
    success_url = reverse_lazy('list')

    # モデルをDBから取得し変数に代入
    # モデルクラス名.objects.all()をviews.pyに記述。(https://kuma-server.com/objects-all/)
    # comment_list = Comment.objects.all()

"""
    # get_context_data でcomment_listとしてlist.htmlに値を渡す。(クラスベースビューの場合)
    def get_context_data(self):
        ctxt = super().get_context_data()
        # テンプレートに渡すための変数名作成
        # (https://chuna.tech/detail/46/#i3-2)
        ctxt["comment_list"] = Comment.objects.all()
        return ctxt

    def get_success_url(self):
        return reverse_lazy('list')
"""


"""
# (https://django.kurodigi.com/comment_regist/)
class PostAndCommentView(FormView):
    template_name = 'comment_list.html'
    form_class = CommentCreateForm
    
    def form_valid(self, form):
        # comment = form.save(commit=False) #保存せずオブジェクト生成する
        # comment.topic = Post.objects.get(id=self.kwargs['pk'])
        # comment.no = Comment.objects.filter(topic=self.kwargs['pk']).count() + 1
        # comment.save()
        form.save_with_topic(self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list')
    
    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Post.objects.get(id=self.kwargs['pk'])
        # filterで取得するオブジェクトの条件を指定(QuerySet)
        # 修正(https://yu-nix.com/blog/2020/11/28/django-filter/#Model.objects.filter()%E3%81%AE%E5%9F%BA%E6%9C%AC%E7%9A%84%E3%81%AA%E4%BD%BF%E3%81%84%E6%96%B9)
        ctx['comment_list'] = Comment.objects.filter(
                ).all
        return ctx
"""