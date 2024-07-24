from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import UserInformation
from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import random
import string
from .models import EmailConfirmation
from .forms import EmailConfirmationForm
import calendar


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
            profile_picture = request.FILES.get("profile_picture")
            date_of_birth = request.POST.get("date_of_birth")
            if first_name!=None and last_name!=None and email!=None and specialyty!=None and profile_picture!=None and date_of_birth!=None:
                user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                user.is_active = False
                user.save()
                group = Group.objects.get(name=specialyty)
                group.user_set.add(user)

                user_inf = UserInformation(user=user,
                                            specialyty=specialyty,
                                            profile_picture=profile_picture,
                                            date_of_birth=date_of_birth)
                user_inf.save()
                token = ''.join(random.choices(string.digits, k=8))
                print(datetime.now().minute+10)
                if datetime.now().time().minute+10>59:
                    minute = datetime.now().time().minute-49
                    hour = datetime.now().time().hour + 1
                    if hour>23:
                        hour -= 24
                        day = datetime.now().day + 1
                        _, days_in_month = calendar.monthrange(datetime.now().year, datetime.now().month)
                        if day>days_in_month:
                            day -= days_in_month
                            month = datetime.now().month + 1
                            if month>12:
                                month -= 12
                                year = datetime.now().year + 1
                            else:
                                year = datetime.now().year
                        else:
                            month = datetime.now().month
                    else:
                        day = datetime.now().day
                else:
                    minute = datetime.now().time().minute
                    hour = datetime.now().time().hour
                    day = datetime.now().day
                    month = datetime.now().month
                    year = datetime.now().year

                model = EmailConfirmation(user=user, token=token, expires_at=datetime(year, month, day, hour, minute))
                model.save()
                html_content = render_to_string('email_template.html', {'user_name': username, "token": token,})
                email = EmailMultiAlternatives("DO-NOT-REPLY", '', "zeldinvasya@gmail.com", [email])
                email.attach_alternative(html_content, "text/html")
                email.send()
                return redirect("email-verification", user.id)
            else:
                user = authenticate(request, username=username, password=password)
                
                if user != None:
                    login(request, user)
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

def timer(time, wait):
    if time[0]*3600+time[1]*60+time[2]-wait>=time[0]*3600+time[1]*60+time[2]:
        return True
    else:
        return False

def email_verification(request, user_id):
    if request.method == 'POST':
        form = EmailConfirmationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['token']
            user = User.objects.get(id=user_id)
            try:
                confirmation = EmailConfirmation.objects.get(user=user, token=code)
                if confirmation.is_expired():
                    form.add_error('code', 'The confirmation code has expired')
                else:
                    user = confirmation.user
                    user.is_active = True
                    user.save()
                    confirmation.delete()
                    login(request, user)
                    return redirect('additionaly')
            except EmailConfirmation.DoesNotExist:
                form.add_error('code', 'Invalid confirmation code')
    else:
        form = EmailConfirmationForm()
    return render(request, 'confirm_email.html', {'form': form})

