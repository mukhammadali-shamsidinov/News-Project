from typing import Any

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import News,Category,Photography
from .forms import ContactForms, CommentForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from news_project.custom_permission import OnlyLoggedPermission
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
# News
def newsList(request):
  news = News.publish.all().order_by('-published_time')[:8]
  context = {
    'news_list':news
  }

  return render(request,'news_list.html',context)



def HomePageView(request):
  news = News.publish.all().order_by('-published_time')[:5]
  category = Category.objects.all()
  mahalliy = News.publish.all().filter(category__name='mahaliy').order_by('-published_time')[1:6]
  local_one = News.publish.all().filter(category__name='mahaliy').order_by('-published_time')[:1]
  context = {
    'news':news,
    "category":category,
    'local_news':mahalliy,
    'local_one':local_one
  }
  return render(request,'index.html',context=context)


class homePageView(ListView):
  model = News
  template_name = 'index.html'
  context_object_name = 'news'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['news'] = News.publish.all().order_by('-published_time')[:5]
    context['category'] = Category.objects.all()
    context['local_news'] = News.publish.all().filter(category__name='mahaliy').order_by('-published_time')[:6]
    context['xorij'] = News.publish.all().filter(category__name="xorij").order_by("-published_time")
    context['sport'] = News.publish.all().filter(category__name="sport").order_by("-published_time")
    context['texnologiya'] = News.publish.all().filter(category__name="texnologiya").order_by("-published_time")
    context['photo'] = Photography.objects.all()
   
  
    return context

# def ContactView(request):
#   form = ContactForms(request.POST or None)
#   if request.method == 'POST' and form.is_valid():
#     form.save()
#     return HttpResponse('<h1>Thanks Bro.</h1>')
#   context = {
#     "form":form
#   }
#   return render(request,'contact.html',context)

def ErorPage(request):

  return render(request,'404.html')


class ContactView(TemplateView):

  def get(self,request,*args,**kwargs):
    form = ContactForms()
    context = {
      "form":form
    }
    return render(request,'contact.html',context)
  
  def post(self,request,*args,**kwargs):
    form = ContactForms(request.POST)
    if request.method == 'POST' and form.is_valid():
      form.save()
      return HttpResponse("Thanks bro")
    context = {
      "form":form
    }
    return render(request,'contact.html',context)
  

class localNewsView(ListView):
  model = News
  template_name = 'mahalliy.html'
  context_object_name = 'local_news'

  def get_queryset(self):
    news = self.model.publish.all().filter(category__name="mahaliy")
    return news
  

class sportNewsView(ListView):
  model = News
  template_name = 'sport.html'
  context_object_name = 'sport_news'

  def get_queryset(self):
    news = self.model.publish.all().filter(category__name="sport")
    return news
  
class xorijNewsView(ListView):
  model = News
  template_name = 'xorij.html'
  context_object_name = 'xorij_news'

  def get_queryset(self):
    news = self.model.publish.all().filter(category__name="xorij")
    return news
  
class texchnologyNewsView(ListView):
  model = News
  template_name = 'texno.html'
  context_object_name = 'texno_news'

  def get_queryset(self):
    news = self.model.publish.all().filter(category__name="texnologiya")
    return news

class EditView(OnlyLoggedPermission,UpdateView):
  model = News
  fields = ("title","body","image","category",)
  template_name = "crud/edit.html"

class Delete(OnlyLoggedPermission,DeleteView):
  model = News
  template_name = 'crud/delete.html'
  success_url = reverse_lazy('basic')


class CreateViewPage(OnlyLoggedPermission,CreateView):
  model = News
  template_name = "crud/create.html"
  fields = ('title','slug','image','body','category','status')


@login_required
@user_passes_test(lambda u:u.is_superuser)
def AdminPage(request):
  user_admin = User.objects.filter(is_superuser=True)
  context = {
    'user':user_admin
  }

  return render(request,'admin.html',context)







def detail_Page(request,news):
  news = get_object_or_404(News,slug=news)
  contex = {}
  hit_count = HitCount.objects.get_for_object(news)
  hits = hit_count.hits
  contex['hitcount'] = {"pk": hit_count.pk}
  hit_count_response = HitCountMixin.hit_count(request, hit_count)
  if hit_count_response.hit_counted:
    hits += 1
    contex['hit_counted'] = hit_count_response.hit_counted
    contex['hit_message'] = hit_count_response.hit_message
    contex['total_hits'] = hits
  comments = news.comments.filter(active=True)
  comments_count = comments.count()
  new_comment = None
  if request.method == 'POST':
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.news = news
        new_comment.user = request.user
        new_comment.save()
        comment_form = CommentForm()
  else:
    comment_form = CommentForm()


  context = {
  'news': news,
  'commets_count':comments_count,
  'comments': comments,
  'new_comment': new_comment,
  'comment_form': comment_form
  }
  return render(request,'single_page.html',context)


class SearchPage(ListView):
  model = News
  template_name = 'search_result.html'
  context_object_name = 'yangilik'

  def get_queryset(self):
    query = self.request.GET.get('q')
    new = super().get_queryset()
    return new.filter(
      Q(title__icontains=query) | Q(body__icontains=query)
    )

