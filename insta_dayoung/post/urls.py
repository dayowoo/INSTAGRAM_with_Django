from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name="main"),
    path('post_new/', views.create, name="post_new"),
    path('post_edit/<int:id>', views.update, name="post_edit"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('my_post_list/<str:username>', views.my_post_list, name='my_post_list'),
    path('hashtags/<int:hashtag_id>/', views.hashtags, name='hashtags'),
    path('like/', views.like, name="like"),
    path('hashtags/<int:hashtag_id>', views.hashtags, name='hashtags'),
    path('my_detail/<int:id>', views.my_detail, name="my_detail"),
    path('follow_list/', views.follow_list, name="follow_list"),
    path('search_list/', views.search_list, name="search_list"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)