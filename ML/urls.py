from django.urls import path
from .views import  ViewDetails, ViewRanking


app_name = 'ml'

urlpatterns = [
    #path('', JobList.as_view(), name='listcreate'),
    path('ranks/<int:pk>/',ViewRanking.as_view(),name='viewranking'),
    path('resumedetails/<int:pk>/',ViewDetails.as_view(),name='viewanalysis'),
]