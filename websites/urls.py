
from django.urls import path
from .views import FormClass, ListClass, PostUpdate, CommentForm
from . import views

urlpatterns = [
    path('form/', views.FormClass.as_view(), name='form'),
    path('', views.ListClass.as_view(), name='list'),
    #参考(https://noumenon-th.net/programming/2019/11/19/django-updateview/)
    path('<pk>/update/', views.PostUpdate.as_view(), name='update'),
    path('<pk>/comment/', views.CommentForm.as_view(), name='comments-create'),
    #path('comment/', views.CommentForm.as_view(), name='comments-create'),
]