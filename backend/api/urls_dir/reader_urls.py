from django.urls import path
from api.views.articleViews import *
from api.views.userViews import *
from api.views.commentViews import *

urlpatterns = [
    path('todays-articles/', get_fresh_articles, name='get_fresh_articles'),
    path('articles/', get_articles, name='get_articles'),
    path('article/<int:id>/', get_article, name='get_article'),
    path('create-reader/', create_user, name='create_reader'),
    path('get-authors/', get_authors, name='get_authors'),
    path('get-categories/', get_categories, name='get_categories'),
    path('comments/create/<int:id>/', create_comment, name='create_comment'),
    path('comments/get/<int:id>/', get_comments, name='get_comments'),
    path('comments/delete/<int:id>/', delete_comment, name='delete_comment'),
]