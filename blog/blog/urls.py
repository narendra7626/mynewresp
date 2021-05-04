"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from myapp import views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('post',views.PostViewset,basename='post')
router.register('comment',views.CommentViewset,basename='comment')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('accounts/profile/',views.index),
    path('registration/',views.signupview,name='register'),
    path('accounts/login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('newpost/',views.PostCreateView.as_view(),name='newpost'),
    path('drafts/', views.DraftListView.as_view(), name='drafts'),
    path('post_detail/<int:pk>/',views.PostDetailView.as_view(),name='post_detail'),
    path('post_publish/<int:pk>/',views.post_publish,name='post_publish'),
    path('post_edit/<int:pk>/',views.PostUpdateView.as_view(),name='post_edit'),
    path('post_remove/<int:pk>/',views.PostDeleteView.as_view(),name='post_remove'),
    path('add_comment/<int:pk>/',views.add_comment_post,name='add_comment'),
    path('comment_approve/<int:pk>/',views.comment_approve,name='comment_approve'),
    path('comment_remove/<int:pk>/', views.comment_remove, name='comment_remove'),
    path('search/',views.search,name='search'),
    path('cat_post/<int:cat_id>/',views.cat_post,name='cat_post'),

    path('viewset/',include(router.urls)),
    path('viewset/<int:pk>/',include(router.urls)),

    path('viewsets/',include(router.urls)),
    path('viesets/<int:pk>/',include(router.urls)),


]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
