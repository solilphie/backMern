from email.mime import application
from unicodedata import category
from rest_framework import viewsets
from django.contrib.auth import get_user_model 
from .serializers import UserSerializer
from rest_framework import generics
from jobpost.models import Post

from application.models import Application
from .serializers import PostSerializer,ApplicationSerializer
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework import filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from users.serializers import CustomUserSerializer
from users.models import NewUser 
from django.core.files import File
from django.http import HttpResponse
from rest_framework.decorators import api_view
from backendapi.settings import BASE_DIR, MEDIA_ROOT
class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user

class UserViewSet(viewsets.ModelViewSet):
   #permission_classes = [IsAuthenticated]
   #queryset = NewUser.objects.all() 
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        user = self.request.user.id
        return NewUser.objects.filter(id=user)


class JobList(generics.ListCreateAPIView):
    #permission_classes = [IsAuthenticated]
    #queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    def get_queryset(self):
        user = self.request.user
        if user.usertypes=='employer':
            
            return Post.objects.filter(author=user)
class ViewSpecialJobList(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    #queryset = Post.postobjects.all()
    
    serializer_class = PostSerializer
    def get_queryset(self):
        user=self.request.user
        categoryy=user.categoryy
		#words=categoryy.split()
		
		#return Post.objects.filter(reduce(Q.__and__, [Q(category=s) for s in categoryy.split(' ')]))
        return Post.objects.filter(category = categoryy)
        

@api_view(['GET'])
def DownloadPDF(self, pk):
    path_to_file = MEDIA_ROOT + '/resumes/'+pk
    f = open(path_to_file, 'rb')
    pdfFile = File(f)
    response = HttpResponse(pdfFile.read())
    response['Content-Disposition'] = 'attachment';
    return response


class ViewJoblist(generics.ListCreateAPIView):
    
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    



class JobDetail(generics.RetrieveDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    
    #def get_queryset(self):
    #    slug = self.request.query_params.get('slug', None)
    #    print(slug)
    #    return Post.objects.filter(slug=slug)

class PostListDetailfilter(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['^title']



class CreatePost(generics.CreateAPIView):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostListDetailfilter(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['^slug']

class AdminPostDetail(generics.RetrieveAPIView):
 
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class EditPost(generics.UpdateAPIView):
    
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class DeletePost(generics.RetrieveDestroyAPIView):
    
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class CreateApplication(generics.CreateAPIView):
    
    #queryset = Application.objects.all()
    #serializer_class = ApplicationSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        print(request.data)
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ViewApplications(viewsets.ModelViewSet):
   
    serializer_class = ApplicationSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Application.objects.filter(jobid=pk)
    
    







#for application in Application.objects.all() :

#    f = open("media/"+str(application.resume), 'r')
#   file_content = f.read()
#    f.close()
#    context = {'file_content': file_content}
    



