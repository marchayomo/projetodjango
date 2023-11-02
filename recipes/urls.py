from django.urls import path
from recipes.templates.recipes.views import home


urlpatterns = [
    path('', home),
]
