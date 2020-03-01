from django.urls import path
from . import views


app_name = 'images'

urlpatterns = [
    # create image
    path('create/', views.image_create, name='create'),

    # image detail
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),

    # like image
    path('like/', views.image_like, name='like'),

    # most viewed images
    path('ranking/', views.image_ranking, name='create'),

    # image list
    path('', views.image_list, name='list'),
]
