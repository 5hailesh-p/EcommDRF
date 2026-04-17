from django.urls import path
from .views import ProductView

urlpatterns = [
    path("all/",ProductView.as_view(),name="products" ),
]
