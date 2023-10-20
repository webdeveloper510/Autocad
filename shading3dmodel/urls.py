from django.urls import path
from shading3dmodel.views import *
from shading3dmodel import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='loginin'),
    path('userprofile/', UserProfileView.as_view(),name='userprofile'),
    path('uploadfile/', AutocadAnalysesView.as_view(),name='uploadfile'),
    path('getdata/', CSVFileGEt.as_view(),name='getdata'),
]


