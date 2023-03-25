from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginFrom

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,"'{}' kullanıcısı ile oturum açılmış durumda, yeni kullanıcı kaydı için çıkış yapmanız gerekmektedir.".format(request.user.username))
        return redirect("index")
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username=username)
        newUser.set_password(password)

        newUser.save()

        login(request,newUser)
        messages.add_message(request,messages.SUCCESS,"Başarılı ile '{}' kullanıcısı oluşuturuldu ve oturum açıldı".format(newUser))
        #messages.SUCCESS(request,"Başarılı ile kullanıcı oluşuturuldu.")
        return redirect("index")
    context = {
        "form" : form
    }
    return render(request,"register.html",context)

"""    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username=username)
            newUser.set_password(password)

            newUser.save()

            login(request,newUser)
            messages.add_message(request,messages.SUCCESS,"başarılı işlem.")
            return redirect("index")
        context = {
            "form" : form
        }
        return render(request,"register.html",context)
    else:
        form = RegisterForm()
        context = {
            "form" : form
        }
        return render(request,"register.html",context)"""

def loginUser(request):
    if request.user.is_authenticated:
        messages.add_message(request,messages.WARNING,"'{}' kullanıcısı ile oturum açılmış durumda, farklı bir kullanıcı ile giriş yapmak için çıkış yapınız.".format(request.user.username))
        return redirect("index")
    
    form = LoginFrom(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username,password=password)

        if user is None:
            messages.add_message(request,messages.WARNING,"Kullanıcı adı veya parola yanlış.")
            return render(request,"login.html",context)
        
        messages.add_message(request,messages.SUCCESS,"Başarı ile giriş yapıldı.")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)

def logoutUser(request):
    if request.user.is_authenticated != 1:
        messages.add_message(request,messages.WARNING,"Oturum açılmadı.")
        return redirect("index")
    else:
        logout(request)
        messages.add_message(request,messages.SUCCESS,"Çıkış yapıldı.")
        return redirect("index")