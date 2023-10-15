from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .form import Login, UserRegister, ProfileEdit,UserEdit
from django.contrib.auth import authenticate,login

from .models import Profile


# Create your views here.

def login_user(request):
  if request.method == 'POST':
    form = Login(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      user = authenticate(request,username = data['username'],password=data['password'])
      if user is not None:

        if user.is_active:
          login(request,user)
          return HttpResponse("Login Mufaqiyatli o'tdi")
        else:
          return HttpResponse("Sizni accountiz faol emas")
    else:
      return HttpResponse("User not Found")
  else:
    form = Login()
    return render(request,'account/login.html',context={
    "form":form
    })
        
@login_required
def dashboard(request):
  user = request.user
  profile = Profile.objects.get(user=user)
  context = {
    "user":user,
    "profile":profile
  }
  return render(request,"registration/profile.html",context)

def SingUp(request):
  if request.method == "POST":
    user_form = UserRegister(request.POST)
    if user_form.is_valid():
      new_user = user_form.save(commit=False)
      new_user.set_password(
        user_form.cleaned_data['password']
      )
      new_user.save()
      profile = Profile.objects.create(user=new_user)
      profile.save()

      return render(request,'account/register-done.html',context={
        "new_user":new_user,
        "profile":profile
      })
  else:
    form = UserRegister()
    profile = ProfileEdit()
    return render(request,'account/register.html',context={"form":form,"profile":profile})

# class SingUp(CreateView):
#   form_class = UserCreationForm
#   template_name = 'account/register.html'
#   success_url = reverse_lazy('login')




@login_required
def editProfile(request):
  if request.method == "POST":
    form = UserEdit(instance=request.user,data=request.POST)
    profile = ProfileEdit(instance=request.user,data=request.POST,files=request.FILES)
    if form.is_valid() and profile.is_valid():
      form.save()
      profile.save()
      return redirect('basic')
  else:
    form = UserEdit(instance=request.user)
    profile = ProfileEdit(instance=request.user)

    return render(request,'registration/profileEdit.html',{"form":form,"profile":profile})

