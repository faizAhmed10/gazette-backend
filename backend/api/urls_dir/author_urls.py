from django.urls import path
from api.views.articleViews import *
from api.views.userViews import *

urlpatterns = [
    # Article Paths
    path('create-article/', create_article, name='create_article'),
    path('update-article/<int:id>/', update_article, name='update_article'),
    path('delete-article/<int:id>/', delete_article, name='delete_article'),
    path('todays-articles/', get_fresh_articles, name='get_fresh_articles'),
    path('all-articles/', get_articles, name='get_articles'),
    path('article/<int:id>', get_article, name='get_article'),
    path('get-my-articles/', get_my_articles, name='get_my_articles'),
    path("get-my-profile/", get_my_profile, name="get_my_profile"),
    path('categories/', category_list_create, name='category-list-create'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    # User Paths
    path('create-author/', create_author, name='create_author'),
    path('check-author/', is_author, name='is_author'),
]