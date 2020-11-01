from django.urls import path

from . import views
urlpatterns =[
    path("userdata",views.userData,name="userData"),
    path("productdata",views.productData,name="productData"),
    path("video",views.videoStream,name="videoStream"),
    path("loaddata",views.loadData,name="loadData"),
  
]