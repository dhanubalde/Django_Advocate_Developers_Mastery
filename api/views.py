from rest_framework.decorators import api_view
from rest_framework import status, permissions, generics
from rest_framework import authentication, mixins
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import AdvocateSerializer
from .serializers import CompanySerializer
from .models import Advocate, Company
from auth.mixin import StaffMixinPermissions
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@api_view(['GET'])
def Endpoints_Api_root(request):
    return Response({
        'Advocate Developers': reverse('advocate-list', request=request),
        'Companies': reverse('companies-list', request=request),
    })


class CompanyListCreateView(
        StaffMixinPermissions,
        generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


Companies_list_create_view = CompanyListCreateView.as_view()


class CompanyRetrieveView(
        StaffMixinPermissions,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'pk'
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


Companies_retrieve_view = CompanyRetrieveView.as_view()


class AdvocateRetrieveView(
        StaffMixinPermissions,
        generics.RetrieveUpdateDestroyAPIView):
    queryset = Advocate.objects.all()
    serializer_class = AdvocateSerializer
    lookup_field = 'pk'
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


Advocate_retrieve_view = AdvocateRetrieveView.as_view()


class AdvocateListCreateView(
        StaffMixinPermissions,
        generics.ListCreateAPIView):
    queryset = Advocate.objects.all()
    serializer_class = AdvocateSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.TokenAuthentication
    ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


Advocate_list_create_view = AdvocateListCreateView.as_view()


class CompanyListApiView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query')
        if query is None:
            query = ''
        queryset = Company.objects.filter(name__icontains=query)
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


Companies_list_view = CompanyListApiView.as_view()


class CompanyDetailsApiView(APIView):

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            return Http404

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = CompanySerializer(queryset, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = self.get_object(pk)
        serializer = CompanySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializers.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


Companies_detail_view = CompanyDetailsApiView.as_view()

# Advocate-list apl/advocate/ url


class AdvocateListApiView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query')
        if query is None:
            query = ''
        queryset = Advocate.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = AdvocateSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdvocateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


Advocate_list_view = AdvocateListApiView.as_view()


class AdvocateDetailApiView(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            return Http404

    def get(self, request, username):
        queryset = self.get_object(username)
        serializer = AdvocateSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, username):
        queryset = self.get_object(username)
        serializer = AdvocateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        queryset = self.get_object(username)
        queryset.delete()
        return Response(status=404)


Advocate_detail_view = AdvocateDetailApiView.as_view()


@api_view(['GET', 'POST'])
def Companies_list(request):

    if request.method == 'GET':
        queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def Companies_detail(request, pk):
    try:
        queryset = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return Response('Request Not Found ', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompanySerializer(queryset, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CompanySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def Advocate_list(request):
    """Search Request ->  api/advocate/?query=<Name Seearch>
    """
    if request.method == 'GET':
        query = request.GET.get('query')
        # filterig query stringin "username or bio "
        if query is None:
            query = ''
        queryset = Advocate.objects.filter(
            Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = AdvocateSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdvocateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def Advocate_detail(request, username):
    """ Retrive information about the specified name in the models
    """
    try:
        queryset = Advocate.objects.get(username=username)
    except Advocate.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdvocateSerializer(queryset, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AdvocateSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def Article_list(request):
    """ List articles and Create new articles
    """

    if request.method == 'GET':
        queryset = Article.objects.all()
        serializer = ArticleSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error_messages, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def Article_detail(request, pk):
    """Retreive article and Update new articles and Delete old articles
    """
    try:
        # get id of article if doesnot exist response 404 http response
        queryset = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ArticleSerializer(queryset)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(queryset, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error_messages, status=400)

    elif request.method == 'DELETE':
        queryset.delete()
        return HttpResponse(status=204)
