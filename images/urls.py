from django.urls import path
from . import views


app_name = 'images'

urlpatterns = [
    # create image
    path('create/', views.image_create, name='create'),

    # image detail
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
]
