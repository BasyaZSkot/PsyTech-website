from django.shortcuts import render, redirect
from .forms import UserPsihHelpInfoForm
from django.contrib.auth.models import User
from .models import UserProblems_and_Preferences
from main_page.models import UserInformation
from psihologist_page.models import SessionsDate
import json

# Create your views here.
def additionaly_regular_user(request):
    if request.method == "POST":
        form = UserPsihHelpInfoForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.prefered_method_for_chating = request.POST.get("contacts")
            print(request.POST.get("time-slots"))
            form.prefer_time_slots = request.POST.get("time-slots")
            form.save()
            return redirect("home")
        else:
            print(form.errors.as_data())
    else:
        form = UserPsihHelpInfoForm
    return render(request, "additionaly_regular_user.html", context={
        "form": form
    })

def client_info_page(request, cl_id):
    client = User.objects.get(id=cl_id)

    client_problem_info = UserProblems_and_Preferences.objects.get(user=client)

    client_info = UserInformation.objects.get(user=client)

    client_sessions = SessionsDate.objects.filter(user=client)


    prefer_time_slots = client_problem_info.prefer_time_slots
    prefered_method_for_chatting = json.loads(client_problem_info.prefered_method_for_chating)

    try:
        client_psih = client_sessions[0].psih
    except:
        client_psih = None
    print(prefer_time_slots)

    return render(request, "html_2.0/client_info_page.html", context={
        "client": client,
        "client_info": client_info,
        "client_problem_info": client_problem_info,
        "client_psih": client_psih,
        "prefer_time_slots": prefer_time_slots,
        "prefered_method_for_chatting": prefered_method_for_chatting,
    })

