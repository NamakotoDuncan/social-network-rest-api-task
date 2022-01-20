from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('status', views.ApiStatus.as_view()),  # tested
    path('post', views.PostList.as_view()),  # tested
    path('post/<int:pk>', views.PostDetail.as_view()),  # tested
    path('post/<int:pk>', views.PostUpdate.as_view()),
    path('post/<int:pk>/like', views.PostLike.as_view()),  # tested
    path('post/<int:pk>', views.PostDelete.as_view()),
    path('post-create', views.PostCreate.as_view()),  # tested
    path('signup', views.CreateUser.as_view()),  # tested
    path('login', views.AuthenticateUser.as_view()),  # tested
    path('profile/<int:pk>', views.UserDetail.as_view()),  # tested
]

urlpatterns = format_suffix_patterns(urlpatterns)
