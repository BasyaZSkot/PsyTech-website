from django.shortcuts import render, redirect
from .models import UserInformation
from psihologist_page.models import Summary
import copy
from .models import SystemMessages
from django.contrib.auth.models import User
from chat.models import Message, Chat
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
from .forms import UserInformationForm
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet


def group_validation(user_object, group_name):
    if list(user_object.groups.values_list("name", flat=True))[0]==group_name:
        return True
    else:
        return False

def home_page(request):
    notifications = {'summaries': [],
                     'meeting_messages': [],
                     'user_group': '',
                     'summary_confirmation': None,
                     'my_summary': '',
                     'no_notif': False,
                     'reject_message': None,
                     }
    chats = []
    chat_first_messages = {}
    no_chats = True
    user_info = ""
    no_image = True
    recipient = {}
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            user_info = UserInformation.objects.get(user=request.user)
            if user_info.profile_picture:
                no_image = False
            notifications['user_group'] = list(request.user .groups.values_list("name", flat=True))[0]        
        notif_copy = copy.deepcopy(notifications)

        if request.user.is_superuser:
            all_summaries = Summary.objects.all()
             
            for summary in all_summaries:
                if group_validation(summary.user, "psihologist"):
                    notifications['summaries'].append(summary)
                    notifications["no_notif"] = False
                try:
                    chat = [i for i in Chat.objects.all() if (request.user in i.members.all() and summary.user in i.members.all())][0]
                    first_message = Message.objects.filter(chat=chat)
                    if not first_message:
                        chats.append(chat)
                        chat_first_messages[chat] = ''
                    else:
                        first_message = first_message.reverse()[0]
                        if len(first_message.content) > 7:
                            chat_first_messages[chat] = first_message.message+'...'
                        else:
                            chat_first_messages[chat] = first_message.message
                        chats.append(chat)
                    recipient[chat] = summary.user
                    no_chats = False
                except:
                    pass


        elif group_validation(request.user, "regular user"):
            pass
        #     meeting_messages = Message.objects.filter(recipient=request.user, content='confirm meeting', read_status=False)
        #     for message in meeting_messages:
        #         notifications["meeting_messages"].append(message)


        else:
            my_summary = Summary.objects.get(user=request.user)
            notif_copy['my_summary'] = my_summary
            notifications['my_summary'] = my_summary

            # meeting_messages = Message.objects.filter(recipient=request.user, content="meeting reuqest", read_status=False)
            
            try:
                __object = SystemMessages.objects.get(recipient=request.user, content="summary rejection", read_status=False)
                notifications["summary_confirmation"] = False
                notifications["reject_message"] = __object
            except:
                try:
                    chat = Chat.objects.get(members=(request.user, summary.sender))
                    notifications["summary_confirmation"] = True

                    first_message = Message.objects.filter(chat=chat)
                    
                    if not first_message:
                        chats.append(chat)
                        chat_first_messages[chat] = ''
                    else:
                        first_message = first_message.reverse()[0]
                        if len(first_message.content) > 7:
                            chat_first_messages[chat] = first_message.message+'...'
                        else:
                            chat_first_messages[chat] = first_message.message
                        chats.append(chat)
                    no_chats = False
                except:
                    pass

            # for message in meeting_messages:
            #     notifications["meeting_messages"].append(message)

        if notif_copy == notifications:
            notifications["no_notif"] = True

    psihologysts_info = []
    psihologysts = User.objects.filter(groups__name='confirm psihologyst')
    for psih in psihologysts:
        psihologysts_info.append(UserInformation.objects.get(user=psih))
    print(no_chats)
    return render(request, "index.html", context={"notifications": notifications,
                                                  "psihologysts_info": psihologysts_info,
                                                  "chats": chats,
                                                  "no_chats": no_chats,
                                                  "user_info": user_info,
                                                  "no_image": no_image,
                                                  "first_message": chat_first_messages,
                                                  "user": request.user,
                                                  "recipient": recipient,
                                                  })


def psihologyst_detail_view(request, pk):
    psihologyst = User.objects.get(id=pk)

    psihologyst_inf = Summary.objects.get(user=psihologyst)

    user_inf = UserInformation.objects.get(user=psihologyst)

    return render(request, 'psihologysts_view.html', context={"psihologyst": psihologyst,
                                                      "psihologyst_inf": psihologyst_inf,
                                                      "user_inf": user_inf,
                                                      })

def settings(request):
    summary = False
    user = request.user
    user_information = UserInformation.objects.get(user=user)
    if not user.is_superuser:
        if group_validation(user, "psihologyst") or group_validation(user, "confirm psihologyst") or group_validation(user, "reject psihologyst"):
            summary = Summary.objects.get(user=user)
    
    return render(request, "settings.html", context={
        "user": user,
        "summary": summary,
        "user_information": user_information,
    })

def user_information(request):
    user = request.user
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        user_info = UserInformation.objects.get(user=user)
        user_information.date_of_birth = request.POST.get("date_of_birth")
        user_info.profile_picture = request.FILES.get("profile_picture")
        user_info.save()
        return HttpResponseRedirect(request.path_info)

    username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name
    profile_picture = UserInformation.objects.get(user=user).profile_picture
    date = UserInformation.objects.get(user=user).date_of_birth
    date_of_birth = ""
    if len(str(date.year)) == 3:
        date_of_birth += f"0{date.year}"
    elif len(str(date.year)) == 2:
        date_of_birth += f"00{date.year}"
    elif len(str(date.year)) == 1:
        date_of_birth += f"000{date.year}"
    else:
        date_of_birth += f"{date.year}"
    if len(str(date.month)) < 2:
        date_of_birth += f"-0{date.month}"
    else:
        date_of_birth += f"-{date.month}"
    if len(str(date.day)) < 2:
        date_of_birth += f"-0{date.day}"
    else:
        date_of_birth += f"-{date.day}"

    return render(request, "user_information_changing.html", context={"username": username, 
                                                                      "email": email, 
                                                                      "first_name": first_name, 
                                                                      "last_name": last_name, 
                                                                      "profile_picture": profile_picture, 
                                                                      "date_of_birth": date_of_birth})

def summary_settings(request):
    summary = Summary.objects.get(user=request.user)
    if request.method == "POST":
        summary.degree = request.POST.get("degree")
        summary.universyty = request.POST.get("universyty")
        if request.FILES.get("diploma") != None:
            summary.diploma = request.FILES.get("diploma")
        summary.training = request.POST.get("training")
        summary.advanced_curses = request.POST.get("advanced_curses")
        summary.description = request.POST.get("description")
        summary.science_interestings = request.POST.get("science_interestings")
        summary.achievements = request.POST.get("achievements")
        summary.work_area = request.POST.get("work_area")
        summary.often_questions = request.POST.get("often_questions")
        summary.experience = request.POST.get("experience")
        summary.something_to_add = request.POST.get("something_to_add")
        summary.save()
        return redirect("home")
    degree = summary.degree
    universyty = summary.universyty
    diploma = summary.diploma
    training = summary.training
    advanced_curses = summary.advanced_curses
    description = summary.description
    science_interestings = summary.science_interestings
    achievements = summary.achievements
    work_area = summary.work_area
    often_questions = summary.often_questions
    experience = summary.experience
    something_to_add = summary.something_to_add
    return render(request, "summary_set.html", context={"degree": degree,
                                                     "universyty": universyty,
                                                     "diploma": diploma,
                                                     "training": training,
                                                     "advanced_curses": advanced_curses,
                                                     "description": description,
                                                     "science_interestings": science_interestings,
                                                     "achievements": achievements,
                                                     "work_area": work_area,
                                                     "often_questions": often_questions,
                                                     "experience": experience,
                                                     "something_to_add": something_to_add,
                                                    })

def change_password(request):
    username = request.user.username
    if request.method == "POST":
        password1 = request.POST.get("password1")
        # password2 = request.POST.get("password2")
        user = request.user
        user.password = password1
        user.save()
        user = authenticate(request, username=username, password=password1)
        login(request, user)
        return redirect("settings")
    return render(request, "change_password.html")

def additionaly(request):
    if not request.user.is_superuser:
        try:
            user_info = UserInformation.objects.get(user=request.user)
            return redirect("home")
        except UserInformation.DoesNotExist:
            if request.method == "POST":
                form = UserInformationForm(request.POST, request.FILES)
                if form.is_valid():
                    form.clean()
                    specialyty = form.cleaned_data["specialyty"]
                    form = form.save(commit=False)
                    form.user = request.user
                    form.save()
                    my_group = Group.objects.get(name=specialyty) 
                    my_group.user_set.add(request.user)

                    if specialyty == "regular user":
                        return redirect("home")
                    elif specialyty == "psihologist":
                        return redirect("filling_summary")
            else:
                form = UserInformationForm
            return render(request, "additionaly.html", context={'form': form})
    else:
        return redirect("home")