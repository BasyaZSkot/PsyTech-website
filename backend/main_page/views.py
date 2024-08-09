from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import UserInformation, Subscribe, SystemMessages
from psihologist_page.models import Summary, FreePlaces
from chat.models import Message, Chat
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import UserInformationForm

from backend.settings import SUBSCRIBE_PRICE

import copy
from datetime import timedelta, datetime
import json


@login_required(login_url='/accounts/login/')
def pay(request, subscribe_time):
    duration = SUBSCRIBE_PRICE[subscribe_time]["duration"]
    if duration != 0:
        obj = Subscribe.objects.create(user=request.user, subscribe=subscribe_time, duration=timedelta(days=duration), session_num=SUBSCRIBE_PRICE[subscribe_time]["sessions"])
    else:
        obj = Subscribe.objects.create(user=request.user, subscribe=subscribe_time, duration=timedelta(days=365), sessions_num=1)
    return redirect("home")

def group_validation(user_object, group_name):
    if list(user_object.groups.values_list("name", flat=True))[0]==group_name:
        return True
    else:
        return False
    
@login_required(login_url='/accounts/login/')
def superuser(request, notifications):
    chats = []
    chat_first_messages = {}
    recipient = {}
    all_summaries = Summary.objects.all()
    no_chats = True
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
                if len(first_message.message) > 7:
                    chat_first_messages[chat] = first_message.message+'...'
                else:
                    chat_first_messages[chat] = first_message.message
                    
                chats.append(chat)
                recipient[chat] = summary.user
                no_chats = False
        except:
            pass

    return chats, no_chats, chat_first_messages, recipient, notifications

@login_required(login_url='/accounts/login/')
def psihologyst(request, notifications, notif_copy):
    chats = []
    chat_first_messages = {}
    recipient = {}
    no_chats = True
    my_summary = Summary.objects.get(user=request.user)
    notif_copy['my_summary'] = my_summary
    notifications['my_summary'] = my_summary
    messages = SystemMessages.objects.filter(recipient=request.user)
    delete_session_date = []
    change_session_date = []
    new_session_date = []
    senders = {}
    session_chats = []
    for i in messages:
        try:
            for l, j in json.loads(i.content)[0].items():
                if l=="delete":
                    delete_session_date.append(j)
                elif l=="change":
                    change_session_date.append(j)
                    chat = [_ for _ in Chat.objects.all() if (request.user in _.members.all() and i.sender in _.members.all())][0]
                    session_chats.append([j, chat])
                elif l=="new":
                    new_session_date.append(j)
                    chat = [i for i in Chat.objects.all() if (request.user in i.members.all() and __object.sender in i.members.all())][0]
                    session_chats.append([j, chat])
                senders[j] = i.sender
        except:
            pass

    try:
        __object = SystemMessages.objects.get(recipient=request.user, content="summary rejection", read_status=False)
        notifications["summary_confirmation"] = False
        notifications["reject_message"] = __object
    except:
        try:
            __object = SystemMessages.objects.get(recipient=request.user, content="summary confirmation")
            chat = [i for i in Chat.objects.all() if (request.user in i.members.all() and __object.sender in i.members.all())][0]

            notifications["summary_confirmation"] = True

            first_message = Message.objects.filter(chat=chat)
                    
            if not first_message:
                chats.append(chat)
                chat_first_messages[chat] = ''
            else:
                first_message = first_message.reverse()[0]
                if len(first_message.message) > 7:
                    chat_first_messages[chat] = first_message.message+'...'
                else:
                    chat_first_messages[chat] = first_message.message
                chats.append(chat)
                recipient[chat] = __object.sender
                no_chats = False
        except:
            pass

    return session_chats, senders, notif_copy, chats, no_chats, chat_first_messages, recipient, notifications, delete_session_date, change_session_date, new_session_date


def home_page(request):
    notifications = {'summaries': [],
                     'user_group': '',
                     'summary_confirmation': None,
                     'my_summary': '',
                     'no_notif': False,
                     'reject_message': None,
                     }
    user_info = ""
    no_image = True
    recipient = {}
    chats = None
    no_chats = None
    chat_first_messages = None
    group = None
    subscribe = None
    delete_session_date = None
    change_session_date = None
    new_session_date = None
    senders = None
    session_chats = None
    if request.user.is_authenticated:
        try:
            subscribe = Subscribe.objects.get(user=request.user)
        except:
            subscribe = None
        if not request.user.is_superuser:
            try:
                user_info = UserInformation.objects.get(user=request.user)
            except:
                redirect("additionaly")

            if user_info.profile_picture:
                no_image = False
            notifications['user_group'] = list(request.user .groups.values_list("name", flat=True))[0]        
        notif_copy = copy.deepcopy(notifications)

        if request.user.is_superuser:
            chats, no_chats, chat_first_messages, recipient, notifications = superuser(request, notifications)

        elif group_validation(request.user, "regular user"):
            pass

        if group_validation(request.user, "confirm psihologist") or group_validation(request.user, "reject psihologist") or group_validation(request.user, "psihologist"):
            group = "psih"
            session_chats, senders, notif_copy, chats, no_chats, chat_first_messages, recipient, notifications, delete_session_date, change_session_date, new_session_date = psihologyst(request, notifications, notif_copy)
        if notif_copy == notifications:
            notifications["no_notif"] = True

    psihologysts_info = []
    psihologysts = User.objects.filter(groups__name='confirm psihologist')
    for psih in psihologysts:
        psihologysts_info.append(UserInformation.objects.get(user=psih))
    prices_for_subscribe = SUBSCRIBE_PRICE
    
    return render(request, "index.html", context={"notifications": notifications,
                                                  "psihologysts_info": psihologysts_info,
                                                  "chats": chats,
                                                  "no_chats": no_chats,
                                                  "user_info": user_info,
                                                  "no_image": no_image,
                                                  "first_message": chat_first_messages,
                                                  "user": request.user,
                                                  "recipient": recipient,
                                                  "subscribes": prices_for_subscribe,
                                                  "group": group,
                                                  "subscribe": subscribe,
                                                  "delete_session_date":delete_session_date,
                                                  "change_session_date":change_session_date,
                                                  "new_session_date":new_session_date,
                                                  "senders": senders,
                                                  "session_chats": session_chats
                                                  })


def psihologyst_detail_view(request, pk):
    psihologyst = User.objects.get(id=pk)

    psihologyst_inf = Summary.objects.get(user=psihologyst)

    user_inf = UserInformation.objects.get(user=psihologyst)

    return render(request, 'psihologysts_view.html', context={"psihologyst": psihologyst,
                                                      "psihologyst_inf": psihologyst_inf,
                                                      "user_inf": user_inf,
                                                      })
@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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