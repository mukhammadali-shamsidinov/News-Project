from django.urls import path
from .views import newsList,detail_Page,HomePageView,ContactView,ErorPage,\
  homePageView,localNewsView, sportNewsView,xorijNewsView,texchnologyNewsView,\
  EditView,Delete,CreateViewPage,AdminPage,SearchPage



urlpatterns = [
  path('local/',localNewsView.as_view(),name="local_news_page"),
  path('sport/',sportNewsView.as_view(),name="sport_news_page"),
  path('xorij/',xorijNewsView.as_view(),name="xorij_news_page"),
  path('texno/',texchnologyNewsView.as_view(),name="technology_news_page"),
  path('create/',CreateViewPage.as_view(),name="create_news_page"),
  path('<slug>/edit',EditView.as_view(),name="edit_news_page"),
  path('adminpage/', AdminPage, name="admin_page"),
  path('<slug>/delete',Delete.as_view(),name="delete_news_page"),
    path('contact-us/',ContactView.as_view(),name="contact_page"),
  path('searchpage/', SearchPage.as_view(), name="search_result"),
  path('error/',ErorPage,name="404_page"),
  path('<slug:news>/',detail_Page,name="news_detail"),
  path('',homePageView.as_view(),name="basic"),


]