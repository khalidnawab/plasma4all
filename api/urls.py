from django.urls import include, path
from . import views

urlpatterns = [
    path('lists/<int:action>', views.get_list),
    path('', include('rest_auth.urls')),
    path('<int:pk>/<int:action>', views.request_plasma),
    path('register/', views.UserCreate.as_view()),
    path('addpatient/', views.add_patient),
]
