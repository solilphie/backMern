from getpass import getuser
from django.urls import path
from .views import JobList, JobDetail, CreatePost, EditPost, AdminPostDetail, DeletePost,PostListDetailfilter, CreateApplication,ViewJoblist,UserViewSet,ViewApplications,ViewSpecialJobList,DownloadPDF


app_name = 'api'

urlpatterns = [
    path('<int:pk>/', JobDetail.as_view(), name='detailcreate'),
    path('', JobList.as_view(), name='listcreate'),
    path('employee/', ViewJoblist.as_view(), name='listcreateemployee'),
    path('admin/create/', CreatePost.as_view(), name='createpost'),
    path('admin/edit/postdetail/<int:pk>/', AdminPostDetail.as_view(), name='admindetailpost'),
    path('admin/edit/<int:pk>/', EditPost.as_view(), name='editpost'),
    path('getuser/',UserViewSet.as_view({'get':'list'}),name='currentuser'),
    path('admin/delete/<int:pk>/', DeletePost.as_view(), name='deletepost'),
    path('search/', PostListDetailfilter.as_view(), name='postsearch'),
    path('admin/apply/', CreateApplication.as_view(), name='createapplication'),
    path('getapplications/',ViewApplications.as_view({'get':'list'}),name='viewapplications'),
    path('getapplications/<int:pk>/',ViewApplications.as_view({'get':'list'}),name='viewapplications'),
    path('specialjoblist/',ViewSpecialJobList.as_view({'get':'list'}),name='specialjoblist'),
    path('download/<str:pk>/', DownloadPDF, name='download_pdf'),

    
    
]