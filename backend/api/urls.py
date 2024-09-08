from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views.userViews import *
from .views.articleViews import *
from api.urls_dir.author_urls import *
from api.urls_dir.reader_urls import *
from api.views.userViews import *
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reader/', include('api.urls_dir.reader_urls')),
    path('author/', include('api.urls_dir.author_urls')),
]
