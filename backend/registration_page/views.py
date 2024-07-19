from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import UserInformation
from django.http import HttpResponseRedirect

def reg(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username==None or password==None:
            return HttpResponseRedirect(request.path_info)
        else:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            
            specialyty = request.POST.get("specialyty")
            profile_picture = request.POST.get("profile_picture")
            date_of_birth = request.POST.get("date_of_birth")
            if first_name!=None and last_name!=None and email!=None and specialyty!=None and profile_picture!=None and date_of_birth!=None:
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                group = Group.objects.get(name=specialyty)
                group.user_set.add(user)
                user = authenticate(request, username=username, password=password)

                user_inf = UserInformation(user=user,
                                            specialyty=specialyty,
                                            profile_picture=profile_picture,
                                            date_of_birth=date_of_birth)
                user_inf.save()
            else:
                user = authenticate(request, username=username, password=password)
                
            if user != None:
                login(request, user)
                if first_name!=None:
                    return redirect('additionaly')
                else:
                    return redirect("home")
        
    return render(request, 'login_reg.html')

def logout_func(request):
    logout(request)
    return redirect('home')

def additionaly(request):
    if list(request.user.groups.values_list("name", flat=True))[0]=='psihologyst':
        return redirect("filling_summary")
    else:
        return redirect("home")
    

