from django.urls import path
from .views import(
    ProfileListView,
    ProfileCreateView,
    ProfileDetailView,
    ProfileUpdateView,
)

urlpatterns= [
    path('', ProfileListView.as_view(), name="profile_list"),
    path('<int:pk>/', ProfileDetailView.as_view(), name="profile_detail"),
    path('create/', ProfileCreateView.as_view(), name="profile_create"),
    path('update/<int:pk>/', ProfileUpdateView.as_view(), name="profile_update"),
]