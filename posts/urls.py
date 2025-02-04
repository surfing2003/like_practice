from django.urls import path
from .views import *

app_name="posts"
urlpatterns = [
    path('new/', new, name="new"),
    path('create/', create, name="create"),
    path('', main, name="main"),
    path('<int:post_id>/', show, name="show"),
    path('<int:post_id>/edit/', update, name="update"),
    path('<int:post_id>/delete/', delete, name="delete"),
    path('<int:post_id>/create_comment', create_comment, name="create_comment"),

    path('<int:post_id>/post_like', post_like, name="post_like"),
    path('like_list/', like_list, name="like_list"),
]