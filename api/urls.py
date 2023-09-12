from django.urls import path
from api import views
# from api.views import Advocate_list_view, Advocate_detail_view
# from api.views import Companies_list, Companies_detail
urlpatterns = [

    path('', views.Endpoints_Api_root),
    path('api/advocate/', views.Advocate_list_create_view, name='advocate-list'),
    path('api/advocate/<int:pk>/', views.Advocate_retrieve_view),




    path('api/company/', views.Companies_list_create_view, name='companies-list'),
    path('api/company/<int:pk>/', views.Companies_retrieve_view)

]
