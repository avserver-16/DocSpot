from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.TweetListView.as_view(), name='tweet_list'),
    path("create/", views.TweetCreateView.as_view(), name='tweet_create'),
    path("<int:pk>/edit/", views.TweetUpdateView.as_view(), name='tweet_update'),
    path("<int:pk>/delete/", views.TweetDeleteView.as_view(), name='tweet_delete'),
    path("register/", views.register, name='register'),
    path("api/search/", views.search_documents, name='search_documents'),
]