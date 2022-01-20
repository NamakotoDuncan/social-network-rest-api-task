from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('status', views.ApiStatus.as_view()),
    path('post', views.PostList.as_view()),
    path('post/<int:pk>', views.PostDetail.as_view()),
    path('post/<int:pk>', views.PostUpdate.as_view()),
    path('post/<int:pk>/like', views.PostLike.as_view()),
    path('post/<int:pk>', views.PostDelete.as_view()),
    path('post-create', views.PostCreate.as_view()),
    path('signup', views.CreateUser.as_view()),
    path('login', views.AuthenticateUser.as_view()),
    path('profile/<int:pk>', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
